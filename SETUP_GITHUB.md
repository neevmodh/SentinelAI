# 🚀 Setting Up Your GitHub Repository

Follow these steps to push your SentinelAI project to GitHub:

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `sentinelai` or `SentinelAI`
   - **Description**: "Early-Warning & Teach-Back Cyber Defense Engine with 98.65% accuracy"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 2: Configure Git (First Time Only)

If you haven't configured Git before, set your name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Connect to GitHub

Copy the commands from GitHub's "push an existing repository" section, or use these:

```bash
# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/sentinelai.git

# Verify the remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 4: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md will be displayed on the main page

## Step 5: Add Topics (Optional but Recommended)

On your GitHub repository page:
1. Click the ⚙️ gear icon next to "About"
2. Add topics/tags:
   - `machine-learning`
   - `cybersecurity`
   - `phishing-detection`
   - `flask`
   - `python`
   - `scikit-learn`
   - `education`
   - `nlp`
   - `threat-detection`
   - `security-awareness`

## Step 6: Enable GitHub Pages (Optional)

If you want to host documentation:
1. Go to Settings → Pages
2. Select source: `main` branch
3. Choose folder: `/docs` or root
4. Save

## Step 7: Add Repository Badges

Update your README.md with actual badges:

```markdown
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/sentinelai?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/sentinelai?style=social)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/sentinelai)
![GitHub license](https://img.shields.io/github/license/YOUR_USERNAME/sentinelai)
```

## Common Issues & Solutions

### Issue: Permission Denied (publickey)
**Solution**: Set up SSH keys or use HTTPS with personal access token
```bash
# Use HTTPS instead
git remote set-url origin https://github.com/YOUR_USERNAME/sentinelai.git
```

### Issue: Large Files
**Solution**: If spam.csv is too large (>100MB), add it to .gitignore
```bash
echo "spam.csv" >> .gitignore
git rm --cached spam.csv
git commit -m "Remove large dataset file"
```

### Issue: Authentication Failed
**Solution**: Use a Personal Access Token instead of password
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

## Next Steps

After pushing to GitHub:

1. ✅ Add a detailed description
2. ✅ Add topics/tags
3. ✅ Create a GitHub Pages site (optional)
4. ✅ Add screenshots to README
5. ✅ Create releases/tags for versions
6. ✅ Set up GitHub Actions for CI/CD (optional)
7. ✅ Add a CHANGELOG.md file
8. ✅ Create issues for future enhancements
9. ✅ Share your project!

## Useful Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-name

# Push a branch
git push origin feature-name

# Pull latest changes
git pull origin main

# View remote repositories
git remote -v

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

## Repository Best Practices

1. **Write clear commit messages**
   ```bash
   git commit -m "Add feature: cognitive manipulation detector"
   ```

2. **Use branches for features**
   ```bash
   git checkout -b feature/new-visualization
   ```

3. **Keep commits atomic** (one logical change per commit)

4. **Update README** when adding features

5. **Tag releases**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

## Need Help?

- [GitHub Documentation](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Community](https://github.community)

---

**Ready to share your amazing cybersecurity project with the world! 🛡️**
