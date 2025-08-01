# Supply & Demand Matching Tool

This project provides an automated solution for matching supply (available associates) with demand (job requisitions) based on skills, grades, and other criteria.

## Features

- **Automated Skill Matching**: Uses intelligent algorithms to match primary and secondary skills between demand and supply
- **Grade Compatibility**: Ensures associates have appropriate grade levels for the requirements
- **Web Interface**: User-friendly HTML application for uploading CSV files and viewing results
- **Downloadable Reports**: Generate CSV reports with detailed matching rationale

## Files

1. **simple_match.py** - Python script for command-line matching
2. **supply_demand_matcher.html** - Web application for interactive matching
3. **analyze_and_match.py** - Advanced matching script (requires additional dependencies)

## Usage

### Option 1: Web Application (Recommended)
1. Open `supply_demand_matcher.html` in your web browser
2. Upload your Demand.csv and Supply.csv files
3. Click "Process Matching" to run the algorithm
4. View results and download the matched CSV file

### Option 2: Python Script
```bash
python simple_match.py
```

## Input File Requirements

### Demand.csv
Required columns:
- `Requisition ID`
- `Primary Skillset Entered`
- `Secondary Skillset Entered`
- `Grade`

### Supply.csv
Required columns:
- `Associate ID`
- `Associate Name`
- `TMP Release status`
- `My SKILLS`
- `PMO Skills`
- `Grade`

## Output

The tool generates a CSV file with these columns:
- **Requisition ID**: Original demand requirement ID
- **Primary Skill**: Required primary skill
- **Secondary Skill**: Required secondary skill  
- **Associate ID**: Matched associate ID
- **Associate Name**: Matched associate name
- **My Skills**: Associate's skills
- **Grade**: Associate's grade
- **Reason**: Detailed rationale for the match

## Matching Algorithm

The tool uses a sophisticated matching algorithm that:

1. **Skill Matching**: 
   - Cleans and normalizes skill descriptions
   - Matches primary skills (60% weight) and secondary skills (40% weight)
   - Uses fuzzy string matching for flexible skill comparison

2. **Grade Compatibility**:
   - Ensures associates meet or exceed required grade levels
   - Grade hierarchy: AD > SM > M > SA > A2 > A1

3. **Scoring System**:
   - Primary skill match: 60 points
   - Secondary skill match: 40 points
   - Grade compatibility bonus: 20 points
   - Minimum threshold: 30 points

## Statistics

The application provides comprehensive statistics including:
- Total demands processed
- Successfully matched demands
- Unmatched demands
- Overall match rate percentage

## Browser Compatibility

The web application is compatible with:
- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+

## Technical Dependencies

- **Python Version**: 3.6+
- **Required Libraries**: pandas, numpy
- **Optional Libraries**: fuzzywuzzy, python-levenshtein (for enhanced matching)
- **Web Dependencies**: PapaParse.js (loaded via CDN)

---

# GitHub Repository Setup Instructions

Follow these steps to upload your project to GitHub:

## Prerequisites
1. Install Git on your computer
2. Create a GitHub account at https://github.com
3. Install GitHub Desktop (optional but recommended for beginners)

## Method 1: Using GitHub Desktop (Recommended for beginners)

### Step 1: Create a New Repository on GitHub
1. Go to https://github.com
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `supply-demand-matching-tool`
   - **Description**: `Automated tool for matching supply and demand based on skills and grades`
   - **Visibility**: Choose Public or Private
   - **Initialize**: Check "Add a README file"
5. Click "Create repository"

### Step 2: Clone Repository to Local Machine
1. On your new repository page, click the green "Code" button
2. Click "Open with GitHub Desktop"
3. Choose a local folder to store the project
4. Click "Clone"

### Step 3: Add Your Files
1. Navigate to the cloned folder on your computer
2. Copy all your project files into this folder:
   - `Demand.csv`
   - `Supply.csv`
   - `simple_match.py`
   - `supply_demand_matcher.html`
   - `analyze_and_match.py`
   - `README.md` (replace the existing one)

### Step 4: Commit and Push Changes
1. Open GitHub Desktop
2. You'll see all your new files in the "Changes" tab
3. Add a commit message like "Initial project upload with matching tool and web interface"
4. Click "Commit to main"
5. Click "Push origin" to upload to GitHub

## Method 2: Using Command Line

### Step 1: Create Repository on GitHub
Follow the same steps as Method 1, Step 1

### Step 2: Clone and Setup Local Repository
```bash
# Navigate to your project directory
cd "c:\Users\161559\OneDrive - Cognizant\Desktop\Vibe Coding\D&S"

# Initialize Git repository
git init

# Add GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/supply-demand-matching-tool.git

# Create and switch to main branch
git branch -M main
```

### Step 3: Add Files and Commit
```bash
# Add all files to staging
git add .

# Commit changes
git commit -m "Initial project upload with matching tool and web interface"

# Push to GitHub
git push -u origin main
```

## Method 3: Upload Files Directly (Simple but limited)

### Step 1: Create Repository
Follow Method 1, Step 1

### Step 2: Upload Files via Web Interface
1. On your repository page, click "uploading an existing file"
2. Drag and drop your files or click "choose your files"
3. Add a commit message
4. Click "Commit changes"

## Best Practices for GitHub

### Repository Structure
```
supply-demand-matching-tool/
├── README.md
├── simple_match.py
├── analyze_and_match.py
├── supply_demand_matcher.html
├── sample_data/
│   ├── Demand.csv
│   └── Supply.csv
├── docs/
│   └── user_guide.md
└── .gitignore
```

### Create a .gitignore File
Create a `.gitignore` file to exclude unnecessary files:
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env

# Data files (if sensitive)
*.csv
*.xlsx

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### Repository Settings
1. **Branch Protection**: Go to Settings > Branches > Add rule
2. **Issues**: Enable issue tracking for bug reports
3. **Wiki**: Enable wiki for detailed documentation
4. **Pages**: Enable GitHub Pages to host your HTML application

## Sharing Your Repository

### Make Repository Public
1. Go to repository Settings
2. Scroll to "Danger Zone"
3. Click "Change repository visibility"
4. Select "Make public"

### Share the Live Application
If you enable GitHub Pages:
1. Go to Settings > Pages
2. Select source branch (usually `main`)
3. Your HTML application will be available at:
   `https://YOUR_USERNAME.github.io/supply-demand-matching-tool/supply_demand_matcher.html`

## Collaboration Features

### Issues and Project Management
- Use Issues to track bugs and feature requests
- Create Labels for categorizing issues
- Use Projects for kanban-style task management

### Pull Requests
- Enable branch protection to require pull requests
- Set up code review requirements
- Use automated testing with GitHub Actions

## Security Considerations

### Sensitive Data
- Never commit sensitive data like employee information
- Use sample/anonymized data for public repositories
- Consider using Git LFS for large files

### Access Control
- Use private repositories for internal tools
- Set up team permissions for organization repositories
- Enable two-factor authentication

## Additional Resources

- [GitHub Documentation](https://docs.github.com)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)
- [GitHub Desktop Guide](https://docs.github.com/en/desktop)
- [Markdown Guide](https://guides.github.com/features/mastering-markdown/)

---

## Troubleshooting

### Common Issues
1. **Large file uploads**: Use Git LFS for files > 100MB
2. **Authentication errors**: Use personal access tokens instead of passwords
3. **Merge conflicts**: Use GitHub Desktop or git mergetool to resolve

### Getting Help
- GitHub Community Forum
- Stack Overflow
- GitHub Support (for paid accounts)
