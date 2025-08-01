import csv
import re
from collections import defaultdict
import os

def clean_skills(skills_text):
    """Clean and extract skills from text"""
    if not skills_text or skills_text == '#N/A' or skills_text.strip() == '':
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
            cleaned_skills.append(skill.strip().lower())
    
    return list(set(cleaned_skills))  # Remove duplicates

def simple_skill_match(demand_skill, supply_skills):
    """Simple skill matching using string containment"""
    demand_skill = demand_skill.lower()
    matches = []
    for supply_skill in supply_skills:
        supply_skill_lower = supply_skill.lower()
        if demand_skill in supply_skill_lower or supply_skill_lower in demand_skill:
            matches.append(supply_skill)
        elif any(word in supply_skill_lower for word in demand_skill.split() if len(word) > 3):
            matches.append(supply_skill)
    return matches

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
        skill_matches = simple_skill_match(primary_skill, all_supply_skills)
        if skill_matches:
            score += 60  # 60 points for primary skill match
            primary_matches.append(f"Primary: {primary_skill} -> {', '.join(skill_matches[:2])}")
    
    # Secondary skill matching (lower weight)
    secondary_matches = []
    for secondary_skill in demand_secondary_clean:
        skill_matches = simple_skill_match(secondary_skill, all_supply_skills)
        if skill_matches:
            score += 40  # 40 points for secondary skill match
            secondary_matches.append(f"Secondary: {secondary_skill} -> {', '.join(skill_matches[:2])}")
    
    matches = primary_matches + secondary_matches
    return score, matches

def grade_compatibility(demand_grade, supply_grade):
    """Check if supply grade is compatible with demand grade"""
    grade_hierarchy = {'AD': 6, 'SM': 5, 'M': 4, 'SA': 3, 'A2': 2, 'A1': 1}
    
    demand_level = grade_hierarchy.get(demand_grade, 0)
    supply_level = grade_hierarchy.get(supply_grade, 0)
    
    # Supply should be equal or higher level than demand
    return supply_level >= demand_level

def read_csv_file(filename):
    """Read CSV file and return list of dictionaries"""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []

def write_csv_file(filename, data, fieldnames):
    """Write data to CSV file"""
    try:
        with open(filename, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"Error writing {filename}: {e}")
        return False

def match_supply_demand(demand_file, supply_file):
    """Main function to match supply with demand"""
    
    # Read CSV files
    print("Reading CSV files...")
    demand_data = read_csv_file(demand_file)
    supply_data = read_csv_file(supply_file)
    
    if not demand_data:
        print(f"Failed to read demand file: {demand_file}")
        return []
    
    if not supply_data:
        print(f"Failed to read supply file: {supply_file}")
        return []
    
    print(f"Loaded {len(demand_data)} demand records and {len(supply_data)} supply records")
    
    # Filter active supply records
    active_supply = [row for row in supply_data if row.get('TMP Release status', '') == 'Active in TMP']
    print(f"Filtered to {len(active_supply)} active supply records")
    
    # Prepare results
    results = []
    
    # For each demand record, find best matches
    for idx, demand_row in enumerate(demand_data):
        if idx % 100 == 0:
            print(f"Processing demand record {idx+1}/{len(demand_data)}")
        
        requisition_id = demand_row.get('Requisition ID', '')
        primary_skill = demand_row.get('Primary Skillset Entered', '')
        secondary_skill = demand_row.get('Secondary Skillset Entered', '')
        demand_grade = demand_row.get('Grade', '')
        
        best_matches = []
        
        # Score each supply candidate
        for supply_row in active_supply:
            associate_id = supply_row.get('Associate ID', '')
            associate_name = supply_row.get('Associate Name', '')
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
                total_score += 20  # Bonus for grade compatibility
            
            if total_score > 30:  # Minimum threshold
                reason_parts = []
                if skill_matches:
                    reason_parts.append(f"Skill matches: {'; '.join(skill_matches[:3])}")  # Show top 3 matches
                if grade_compatible:
                    reason_parts.append(f"Grade compatible: {supply_grade} >= {demand_grade}")
                else:
                    reason_parts.append(f"Grade mismatch: {supply_grade} vs required {demand_grade}")
                
                reason = "; ".join(reason_parts) if reason_parts else "Basic skill alignment found"
                
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
                'Reason': 'No candidates met the minimum skill match threshold'
            })
    
    # Save to CSV
    output_file = 'supply_demand_matches.csv'
    fieldnames = ['Requisition ID', 'Primary Skill', 'Secondary Skill', 'Associate ID', 
                  'Associate Name', 'My Skills', 'Grade', 'Reason']
    
    if write_csv_file(output_file, results, fieldnames):
        print(f"\nResults saved to {output_file}")
    else:
        print(f"\nFailed to save results to {output_file}")
    
    # Print summary statistics
    matched_count = len([r for r in results if r['Associate ID'] != 'No Match'])
    print(f"\nSummary:")
    print(f"Total demands: {len(results)}")
    print(f"Successfully matched: {matched_count}")
    print(f"No matches found: {len(results) - matched_count}")
    print(f"Match rate: {matched_count/len(results)*100:.1f}%")
    
    return results

if __name__ == "__main__":
    # Check if files exist
    demand_file = 'Demand.csv'
    supply_file = 'Supply.csv'
    
    if not os.path.exists(demand_file):
        print(f"Error: {demand_file} not found in current directory")
        exit(1)
    
    if not os.path.exists(supply_file):
        print(f"Error: {supply_file} not found in current directory")
        exit(1)
    
    # Run the matching algorithm
    print("Supply & Demand Matching Tool")
    print("=" * 40)
    results = match_supply_demand(demand_file, supply_file)
    print("\nMatching completed successfully!")
    print(f"Check 'supply_demand_matches.csv' for detailed results.")
