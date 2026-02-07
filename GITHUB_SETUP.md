# 📦 How to Upload This Project to GitHub

Follow these steps to create a GitHub repository and upload your project.

## Step 1: Create a New Repository on GitHub

1. Go to [GitHub](https://github.com) and login
2. Click the **+** button (top right) → **New repository**
3. Fill in the details:
   - **Repository name:** `CardmarketPokemon` (or any name you prefer)
   - **Description:** `Automated Pokemon card upload bot for Cardmarket with anti-Cloudflare protection`
   - **Public or Private:** Choose based on your preference
   - **DO NOT** initialize with README (we already have one)
   - **DO NOT** add .gitignore (we already have one)
   - **License:** MIT (recommended) or None
4. Click **Create repository**

## Step 2: Initialize Git in Your Local Project

Open a terminal/command prompt in your project folder and run:

```bash
cd D:\CardmarketPokemon

# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Cardmarket Pokemon Bot with Stealth Mode"
```

## Step 3: Connect to GitHub and Push

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/CardmarketPokemon.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### If you get an authentication error:

**Option 1: Use Personal Access Token (Recommended)**

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token (classic)**
3. Select scopes: `repo` (full control of private repositories)
4. Copy the token
5. When git asks for password, paste the token instead

**Option 2: Use SSH**

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add SSH key to GitHub
# Copy the contents of: C:\Users\YOUR_USER\.ssh\id_ed25519.pub
# Go to GitHub → Settings → SSH and GPG keys → New SSH key

# Change remote URL to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/CardmarketPokemon.git

# Push again
git push -u origin main
```

## Step 4: Verify Upload

1. Go to your GitHub repository URL:
   ```
   https://github.com/YOUR_USERNAME/CardmarketPokemon
   ```
2. You should see:
   - ✅ README.md displaying nicely
   - ✅ All Python files
   - ✅ Example CSV
   - ✅ Configuration files
   - ❌ No `chrome_bot_profile/` folder (it's in .gitignore)
   - ❌ No `__pycache__/` folder (it's in .gitignore)

## Step 5: Update README with Your Username

Edit `README.md` and replace `YOUR_USERNAME` with your actual GitHub username in these lines:

```markdown
git clone https://github.com/YOUR_USERNAME/CardmarketPokemon.git
```

Then commit and push the change:

```bash
git add README.md
git commit -m "Update README with correct GitHub username"
git push
```

## Step 6: Add a License (Optional but Recommended)

1. On GitHub, go to your repository
2. Click **Add file** → **Create new file**
3. Name it `LICENSE`
4. Click **Choose a license template**
5. Select **MIT License**
6. Click **Review and submit**
7. Commit the file

## Step 7: Add Topics (Optional)

Make your repo more discoverable:

1. On your repository page, click ⚙️ (settings gear) next to "About"
2. Add topics:
   - `pokemon`
   - `cardmarket`
   - `automation`
   - `playwright`
   - `bot`
   - `anti-detection`
   - `cloudflare-bypass`
   - `stealth`
3. Click **Save changes**

## 🎉 Done!

Your project is now on GitHub!

### Share your repository:
```
https://github.com/YOUR_USERNAME/CardmarketPokemon
```

### Future updates:

When you make changes to the code:

```bash
# Stage changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## 📝 Quick Commands Reference

```bash
# Check status
git status

# See what changed
git diff

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Pull latest changes
git pull

# Push changes
git push
```

## 🆘 Common Issues

### "Permission denied" error
- Use a Personal Access Token instead of password
- Or set up SSH keys (see Step 3)

### "Repository not found" error
- Check the URL is correct
- Make sure you replaced `YOUR_USERNAME` with your actual username

### "Failed to push" error
- Try: `git pull origin main --rebase` then `git push`

### Want to start over?
```bash
rm -rf .git
git init
# Then follow steps 2-3 again
```

---

**Need help?** Open an issue on the repository!
