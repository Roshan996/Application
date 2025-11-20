# 🚀 <span>Git Workflow Guide</span>

This **Git Workflow Guide** is designed to help you and your team collaborate smoothly, avoid common mistakes, and maintain a clean, stable, and professional project structure.

Since you’ve already completed the **installation** steps and have your project set up locally, this guide focuses entirely on **how to work with Git properly** — branching, committing, syncing, resolving conflicts, and teaming up with other developers.

It ensures that every developer follows a consistent workflow, reducing errors and making teamwork faster, cleaner, and more predictable.

---

## ✔️ <span>Requirements</span>

- **Git** installed  
- Access to the remote repository  
- Basic understanding of your project  

---

## 🧭 <span>1. Clone the Repository</span>

```bash
git clone https://github.com/<team>/<project>.git
cd <project>
```


---

## 🌿 <span>2. Create or Switch Branch</span>


**Switch to an existing branch:**

```
git switch branch_name
```

**Create a new branch:**
```
git branch new-branch-name

```
---

## 🔗 <span>3. Set Origin for Pull & Push</span>

Set upstream branches easy and fast working:
```

git branch --set-upstream-to=origin/branch branch


```

> 🟦 Use this when Git says: “No upstream branch set.”

---

## 📋 <span>4. Get All Branches</span>

```

git branch
```


## 🔄 <span>5. Always Sync Before Starting Work</span>
```
git switch main
git pull
git switch your-branch
git merge main

```
> [!WARNING]
> Pulling before pushing prevents conflicts and keeps your branch updated.

---

## ✍️ <span>6. Stage & Commit Changes</span>

**Stage everything:**
```
git add .

Commit changes:

git commit -m "Your message here"

```
---

## 🚚 <span>7. Push Changes to Repository</span>
```
git push
```
> [!NOTE]
> Make sure, you have se origin upstream

First push of a branch:
```
git push -u origin your-branch
```

---

## 📥 <span>8. Pull Latest Changes</span>

```
git pull
```

---

## 🔀 <span>9. Merge Main Into Your Branch</span>

Keep your branch updated with latest changes:

```
git switch main
git pull
git switch your-branch
git merge main
```

---

## ⚔️ <span>10. Handle Merge Conflicts</span>

If you see conflict markers:

```
<<<<<<< HEAD
Your changes
=======
Their changes
>>>>>>> main
```
Fix → save → commit:

```
git add .
git commit -m "Resolve merge conflict"
```

---

## 🤝 <span>11. Team Collaboration Rules</span>

* ✔️ Always create a branch for new work

- ✔️ Always pull before pushing

* ✔️ Keep commit messages clear

* ✔️ Use Pull Requests for merging

* ✔️ Keep main clean & stable

+ ❌ Never work directly on main

* ❌ Never push broken or untested code



---

## 🎯 <span>Conclusion</span>

**Following this workflow ensures:**

* A clean and stable repository

* Less conflicts

* Faster teamwork

* Predictable development flow



---

> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative