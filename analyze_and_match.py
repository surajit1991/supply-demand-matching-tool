import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

def clean_skills(skills_text):
    """Clean and extract skills from text"""
    if pd.isna(skills_text) or skills_text == '' or skills_text == '#N/A':
        return []
    
    # Convert to string and clean
    skills_text = str(skills_text)
    
    # Split by common delimiters
    skills = re.split(r'[,;|&\n\r]', skills_text)
    
    # Clean each skill
    cleaned_skills = []
    for skill in skills:
        # Remove extra whitespace and unwanted characters
        skill = re.sub(r'[^\w\s\.\+\-#]', ' ', skill).strip()
        # Remove experience years patterns
        skill = re.sub(r'\d+\s*(years?|yrs?|experience)', '', skill, flags=re.IGNORECASE).strip()
        # Remove common noise words
        skill = re.sub(r'\b(experience|years?|yrs?|around|approximately)\b', '', skill, flags=re.IGNORECASE).strip()
        
        if skill and len(skill) > 2:  # Only keep meaningful skills
            cleaned_skills.append(skill.strip())
    
    return list(set(cleaned_skills))  # Remove duplicates

def calculate_skill_match_score(demand_primary, demand_secondary, supply_skills, pmo_skills):
    """Calculate skill matching score between demand and supply"""
    score = 0
    matches = []
    
    # Clean skills
    demand_primary_clean = clean_skills(demand_primary)
    demand_secondary_clean = clean_skills(demand_secondary)
    supply_skills_clean = clean_skills(supply_skills)
    pmo_skills_clean = clean_skills(pmo_skills)
    
    all_supply_skills = supply_skills_clean + pmo_skills_clean
    
    # Primary skill matching (higher weight)
    primary_matches = []
    for primary_skill in demand_primary_clean:
        best_match = process.extractOne(primary_skill, all_supply_skills, scorer=fuzz.partial_ratio)
        if best_match and best_match[1] >= 70:  # 70% threshold
            score += best_match[1] * 0.6  # 60% weight for primary skills
            primary_matches.append(f"Primary: {primary_skill} -> {best_match[0]} ({best_match[1]}%)")
    
    # Secondary skill matching (lower weight)
    secondary_matches = []
    for secondary_skill in demand_secondary_clean:
        best_match = process.extractOne(secondary_skill, all_supply_skills, scorer=fuzz.partial_ratio)
        if best_match and best_match[1] >= 70:
            score += best_match[1] * 0.4  # 40% weight for secondary skills
            secondary_matches.append(f"Secondary: {secondary_skill} -> {best_match[0]} ({best_match[1]}%)")
    
    matches = primary_matches + secondary_matches
    return score, matches

def grade_compatibility(demand_grade, supply_grade):
    """Check if supply grade is compatible with demand grade"""
    grade_hierarchy = {'AD': 6, 'SM': 5, 'M': 4, 'SA': 3, 'A2': 2, 'A1': 1}
    
    demand_level = grade_hierarchy.get(demand_grade, 0)
    supply_level = grade_hierarchy.get(supply_grade, 0)
    
    # Supply should be equal or higher level than demand
    return supply_level >= demand_level

def match_supply_demand(demand_file, supply_file):
    """Main function to match supply with demand"""
    
    # Read CSV files
    print("Reading CSV files...")
    demand_df = pd.read_csv(demand_file)
    supply_df = pd.read_csv(supply_file)
    
    print(f"Loaded {len(demand_df)} demand records and {len(supply_df)} supply records")
    
    # Filter active supply records
    supply_df = supply_df[supply_df['TMP Release status'] == 'Active in TMP'].copy()
    print(f"Filtered to {len(supply_df)} active supply records")
    
    # Prepare results
    results = []
    
    # For each demand record, find best matches
    for idx, demand_row in demand_df.iterrows():
        if idx % 100 == 0:
            print(f"Processing demand record {idx+1}/{len(demand_df)}")
        
        requisition_id = demand_row['Requisition ID']
        primary_skill = demand_row.get('Primary Skillset Entered', '')
        secondary_skill = demand_row.get('Secondary Skillset Entered', '')
        demand_grade = demand_row.get('Grade', '')
        
        best_matches = []
        
        # Score each supply candidate
        for _, supply_row in supply_df.iterrows():
            associate_id = supply_row['Associate ID']
            associate_name = supply_row['Associate Name']
            my_skills = supply_row.get('My SKILLS', '')
            pmo_skills = supply_row.get('PMO Skills', '')
            supply_grade = supply_row.get('Grade', '')
            
            # Calculate skill match score
            skill_score, skill_matches = calculate_skill_match_score(
                primary_skill, secondary_skill, my_skills, pmo_skills
            )
            
            # Check grade compatibility
            grade_compatible = grade_compatibility(demand_grade, supply_grade)
            
            # Calculate total score
            total_score = skill_score
            if grade_compatible:
                total_score += 10  # Bonus for grade compatibility
            
            if total_score > 30:  # Minimum threshold
                reason_parts = []
                if skill_matches:
                    reason_parts.append(f"Skill matches: {'; '.join(skill_matches[:3])}")  # Show top 3 matches
                if grade_compatible:
                    reason_parts.append(f"Grade compatible: {supply_grade} >= {demand_grade}")
                else:
                    reason_parts.append(f"Grade mismatch: {supply_grade} vs required {demand_grade}")
                
                reason = "; ".join(reason_parts)
                
                best_matches.append({
                    'associate_id': associate_id,
                    'associate_name': associate_name,
                    'my_skills': my_skills,
                    'grade': supply_grade,
                    'score': total_score,
                    'reason': reason
                })
        
        # Sort by score and take best match
        best_matches.sort(key=lambda x: x['score'], reverse=True)
        
        if best_matches:
            best_match = best_matches[0]
            results.append({
                'Requisition ID': requisition_id,
                'Primary Skill': primary_skill,
                'Secondary Skill': secondary_skill,
                'Associate ID': best_match['associate_id'],
                'Associate Name': best_match['associate_name'],
                'My Skills': best_match['my_skills'],
                'Grade': best_match['grade'],
                'Reason': best_match['reason']
            })
        else:
            # No suitable match found
            results.append({
                'Requisition ID': requisition_id,
                'Primary Skill': primary_skill,
                'Secondary Skill': secondary_skill,
                'Associate ID': 'No Match',
                'Associate Name': 'No Match',
                'My Skills': 'No suitable candidate found',
                'Grade': 'N/A',
                'Reason': 'No candidates met the minimum skill match threshold (30%)'
            })
    
    # Create output DataFrame
    output_df = pd.DataFrame(results)
    
    # Save to CSV
    output_file = 'supply_demand_matches.csv'
    output_df.to_csv(output_file, index=False)
    print(f"\nResults saved to {output_file}")
    
    # Print summary statistics
    matched_count = len(output_df[output_df['Associate ID'] != 'No Match'])
    print(f"\nSummary:")
    print(f"Total demands: {len(output_df)}")
    print(f"Successfully matched: {matched_count}")
    print(f"No matches found: {len(output_df) - matched_count}")
    print(f"Match rate: {matched_count/len(output_df)*100:.1f}%")
    
    return output_df

if __name__ == "__main__":
    # Run the matching algorithm
    results = match_supply_demand('Demand.csv', 'Supply.csv')
    print("\nMatching completed successfully!")
