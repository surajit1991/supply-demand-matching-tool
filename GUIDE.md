# Supply & Demand Matching Tool - Complete Guide

## Project Overview

This project provides an automated solution for matching available associates (supply) with job requisitions (demand) based on skills, experience, and grade compatibility. The tool analyzes CSV data and generates comprehensive matching reports with detailed rationale.

## 📁 Project Structure

```
supply-demand-matching-tool/
├── README.md                          # Complete documentation
├── GUIDE.md                          # This comprehensive guide
├── basic_match.py                    # Standalone Python script (no dependencies)
├── simple_match.py                   # Enhanced Python script (requires pandas)
├── analyze_and_match.py              # Advanced script (requires fuzzywuzzy)
├── supply_demand_matcher.html        # Web application
├── sample_supply_demand_matches.csv  # Example output
├── Demand.csv                        # Input demand data
├── Supply.csv                        # Input supply data
└── docs/                            # Additional documentation
```

## 🚀 Quick Start

### Option 1: Web Application (Recommended)
1. Open `supply_demand_matcher.html` in any modern web browser
2. Upload your `Demand.csv` and `Supply.csv` files
3. Click "Process Matching"
4. Download the results

### Option 2: Python Script
1. Ensure Python is installed on your system
2. Run: `python basic_match.py`
3. Check the generated `supply_demand_matches.csv` file

## 📊 Input Data Requirements

### Demand.csv Format
The demand file should contain these essential columns:
- **Requisition ID**: Unique identifier for each demand
- **Primary Skillset Entered**: Main required skill
- **Secondary Skillset Entered**: Additional required skill
- **Grade**: Required grade level (AD, SM, M, SA, A2, A1)

### Supply.csv Format
The supply file should contain these essential columns:
- **Associate ID**: Unique identifier for each associate
- **Associate Name**: Full name of the associate
- **TMP Release status**: Should be "Active in TMP" for available associates
- **My SKILLS**: Comma-separated list of associate's skills
- **PMO Skills**: Additional skills from PMO database
- **Grade**: Associate's current grade level

## 🔍 Matching Algorithm Details

### 1. Skill Matching Process

The algorithm performs intelligent skill matching through these steps:

#### Data Cleaning
- Removes experience indicators (e.g., "5 years", "yrs")
- Eliminates noise words ("around", "approximately")
- Standardizes skill names (case-insensitive)
- Handles multiple delimiters (comma, semicolon, pipe)

#### Skill Comparison
- **Primary Skills**: 60% weight in scoring
- **Secondary Skills**: 40% weight in scoring
- Uses both exact matches and partial matches
- Considers word-level matching for compound skills

#### Example Matching
```
Demand: "Machine Learning"
Supply: "ML, Machine Learning, Data Science, Python"
Result: ✅ Match found (exact match)

Demand: "Java"
Supply: "Core Java, Spring Boot, J2EE"
Result: ✅ Match found (partial match)
```

### 2. Grade Compatibility

Grade hierarchy (highest to lowest):
```
AD (Architect/Director) = 6
SM (Senior Manager) = 5
M (Manager) = 4
SA (Senior Associate) = 3
A2 (Associate II) = 2
A1 (Associate I) = 1
```

**Rule**: Associate's grade must be ≥ Required grade

### 3. Scoring System

Total Score = Skill Score + Grade Bonus

- **Primary skill match**: +60 points
- **Secondary skill match**: +40 points
- **Grade compatibility**: +20 bonus points
- **Minimum threshold**: 30 points

### 4. Selection Logic

1. Calculate scores for all active associates
2. Filter candidates above threshold (30 points)
3. Sort by total score (descending)
4. Select the highest-scoring candidate
5. If no matches found, mark as "No Match"

## 📈 Output Analysis

### Generated Columns

| Column | Description | Example |
|--------|-------------|---------|
| Requisition ID | Original demand ID | 6191646-1 |
| Primary Skill | Required primary skill | Spark |
| Secondary Skill | Required secondary skill | Hive |
| Associate ID | Matched associate ID | 193089 |
| Associate Name | Matched associate name | Giri, Saikat |
| My Skills | Associate's complete skill set | Data Architecture, AWS, Python... |
| Grade | Associate's grade | AD |
| Reason | Detailed matching rationale | Primary: spark → Data Engineering; Grade compatible: AD ≥ M |

### Sample Reason Explanations

1. **Perfect Match**:
   ```
   Primary: java → Core Java; Secondary: spring → Spring Boot; Grade compatible: SM ≥ SA
   ```

2. **Partial Match**:
   ```
   Primary: machine learning → Data Science; Grade mismatch: SA vs required M
   ```

3. **No Match**:
   ```
   No candidates met the minimum skill match threshold
   ```

## 📊 Statistics Dashboard

The tool provides comprehensive analytics:

### Key Metrics
- **Total Demands**: Number of requirements processed
- **Successfully Matched**: Requirements with assigned associates
- **No Matches Found**: Unmatched requirements
- **Match Rate**: Percentage of successful matches

### Typical Results
- Match rates typically range from 60-85%
- Higher-grade requirements have lower match rates
- Technical skills show better matching than domain skills

## 🛠️ Technical Implementation

### Web Application Features

1. **Drag & Drop Upload**: Intuitive file handling
2. **Real-time Progress**: Visual progress indicators
3. **Interactive Results**: Sortable, filterable tables
4. **Export Functionality**: Download results as CSV
5. **Responsive Design**: Works on desktop and mobile

### Python Script Features

1. **Error Handling**: Robust file reading and validation
2. **Memory Efficient**: Processes large datasets without memory issues
3. **Progress Tracking**: Console progress indicators
4. **Flexible Input**: Handles various CSV formats
5. **Detailed Logging**: Comprehensive status messages

### Performance Optimization

- **Chunk Processing**: Handles large datasets efficiently
- **Smart Caching**: Reuses cleaned skill data
- **Parallel Processing**: Can be extended for multi-threading
- **Memory Management**: Optimized for large files

## 🎯 Best Practices

### Data Preparation
1. **Clean Input Data**: Remove empty rows and invalid characters
2. **Standardize Skills**: Use consistent skill naming conventions
3. **Validate Grades**: Ensure grade values match the hierarchy
4. **Check Status**: Verify "Active in TMP" status for availability

### Optimal Matching
1. **Skill Granularity**: Use specific skill names (e.g., "Python" vs "Programming")
2. **Multiple Skills**: Include both technical and domain skills
3. **Grade Flexibility**: Consider grade ranges rather than exact matches
4. **Regular Updates**: Keep skill databases current

### Result Analysis
1. **Review No Matches**: Identify skill gaps in the organization
2. **Analyze Patterns**: Look for common skill requirements
3. **Quality Check**: Validate high-score matches manually
4. **Feedback Loop**: Use results to improve skill categorization

## 🔧 Customization Options

### Adjusting Scoring Weights
```python
# In the algorithm, modify these values:
PRIMARY_SKILL_WEIGHT = 60    # Default: 60
SECONDARY_SKILL_WEIGHT = 40  # Default: 40
GRADE_BONUS = 20            # Default: 20
MINIMUM_THRESHOLD = 30      # Default: 30
```

### Adding New Grade Levels
```python
grade_hierarchy = {
    'ED': 7,     # Executive Director
    'AD': 6,     # Architect/Director
    'SM': 5,     # Senior Manager
    'M': 4,      # Manager
    'SA': 3,     # Senior Associate
    'A2': 2,     # Associate II
    'A1': 1      # Associate I
}
```

### Custom Skill Categories
You can enhance the matching by adding skill categories:

```python
skill_categories = {
    'programming': ['java', 'python', 'c++', 'javascript'],
    'data': ['sql', 'nosql', 'etl', 'data warehouse'],
    'cloud': ['aws', 'azure', 'gcp', 'docker'],
    'web': ['html', 'css', 'react', 'angular']
}
```

## 🐛 Troubleshooting

### Common Issues

1. **File Not Found Error**
   ```
   Error: Demand.csv not found in current directory
   Solution: Ensure CSV files are in the same folder as the script
   ```

2. **Empty Results**
   ```
   Problem: All matches show "No Match"
   Solution: Check skill naming consistency and threshold settings
   ```

3. **Memory Issues**
   ```
   Problem: Script crashes with large files
   Solution: Use the chunk processing version or increase system memory
   ```

4. **Encoding Problems**
   ```
   Problem: Special characters appear incorrectly
   Solution: Ensure CSV files are saved with UTF-8 encoding
   ```

### Performance Issues

1. **Slow Processing**
   - Reduce batch size in chunk processing
   - Use simpler matching algorithm
   - Consider hardware upgrade

2. **High Memory Usage**
   - Process files in smaller chunks
   - Clear intermediate variables
   - Use streaming CSV readers

## 📱 Web Application Usage

### Step-by-Step Guide

1. **Open Application**: Double-click `supply_demand_matcher.html`
2. **Upload Files**: 
   - Click on demand upload area
   - Select your `Demand.csv` file
   - Repeat for supply file
3. **Process Data**: Click "Process Matching" button
4. **Review Results**: Examine statistics and detailed matches
5. **Download**: Click "Download Results CSV" to save

### Browser Requirements
- Chrome 70+, Firefox 65+, Safari 12+, Edge 79+
- JavaScript enabled
- Local file access permissions

### Troubleshooting Web App

1. **Upload Fails**: Check file size (limit: 100MB) and format
2. **Processing Hangs**: Refresh page and try smaller files
3. **Display Issues**: Try different browser or disable ad blockers

## 🚀 Advanced Features

### Batch Processing
For multiple demand/supply combinations:

```python
# Process multiple file pairs
file_pairs = [
    ('Q1_Demand.csv', 'Q1_Supply.csv'),
    ('Q2_Demand.csv', 'Q2_Supply.csv'),
    ('Q3_Demand.csv', 'Q3_Supply.csv'),
]

for demand_file, supply_file in file_pairs:
    results = match_supply_demand(demand_file, supply_file)
    # Process results...
```

### Integration Options

1. **Database Integration**: Connect to HR databases
2. **API Development**: Create REST API for real-time matching
3. **Scheduling**: Automate periodic matching runs
4. **Notification System**: Alert managers of new matches

### Reporting Enhancements

1. **Dashboard Creation**: Build executive dashboards
2. **Trend Analysis**: Track matching patterns over time
3. **Skill Gap Analysis**: Identify missing skills in organization
4. **Performance Metrics**: Monitor matching efficiency

## 📊 Sample Use Cases

### Scenario 1: Project Staffing
```
Input: 50 new project requirements
Process: Match with 200 available consultants
Output: 85% match rate, 42 successful assignments
Benefit: Reduced staffing time from weeks to hours
```

### Scenario 2: Skill Gap Analysis
```
Input: Quarterly demand forecast
Process: Analyze unmatched requirements
Output: List of skills to recruit/train
Benefit: Proactive workforce planning
```

### Scenario 3: Resource Optimization
```
Input: Bench strength data + upcoming projects
Process: Pre-match resources to future needs
Output: Optimized resource allocation
Benefit: Reduced bench time, improved utilization
```

## 🔮 Future Enhancements

### Planned Features
1. **Machine Learning**: AI-powered skill similarity detection
2. **Real-time Matching**: Live updates as data changes
3. **Mobile App**: Native mobile applications
4. **Integration APIs**: Connect with popular HR systems

### Advanced Algorithms
1. **Semantic Matching**: Understand skill relationships
2. **Learning System**: Improve matching based on feedback
3. **Multi-criteria Optimization**: Balance multiple factors
4. **Predictive Modeling**: Forecast future matching success

## 💡 Tips for Success

### Data Quality
- Maintain consistent skill vocabularies
- Regular data cleanup and validation
- Standardize naming conventions
- Keep availability status current

### Process Integration
- Train users on tool capabilities
- Establish matching workflows
- Create feedback mechanisms
- Monitor and improve continuously

### Organizational Adoption
- Start with pilot projects
- Demonstrate value with metrics
- Provide user training
- Gather stakeholder feedback

---

## 📞 Support and Contact

For questions, issues, or enhancements:
- Check the troubleshooting section
- Review sample data formats
- Test with smaller datasets first
- Document any issues for future reference

Remember: The tool is designed to assist decision-making, not replace human judgment. Always review matches before final assignments!
