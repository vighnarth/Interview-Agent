# Research Paper: SkillBridgeAI Framework

**Title**: Real-Time AI-Based Skill Gap Analysis and Adaptive Career Guidance Using a Generative AI Framework for the Modern Job Market  
**Publication**: IEEE 5th ASIANCON 2025  
**Authors**: Vighnarth Nile (Lead Author), Sharmila Sengupta, Soham Parab, Sushanth Shetty, Atharva Sambhaji

---

## Abstract & Core Objective
The research addresses the limitations of traditional career guidance (generic recommendations and static keyword filters) by introducing **SkillBridgeAI**. The platform leverages Generative AI to integrate dynamic competency testing, real-time skill gap analysis, and automated resume tailoring into a single adaptive ecosystem.

---

## Key Technical Contributions
1.  **Generative AI Integration**: Utilized the **Gemini Flash 1.5** model to move beyond keyword matching to a "rich understanding" of candidate abilities based on experience, verified skills, and project portfolios.
2.  **Benchmarking Dataset**: Designed a specialized dataset for four key roles: **Full Stack Developer, AI/ML Engineer, Cloud & DevOps Engineer, and Software Engineer**.
3.  **Authentication & Integrity**: Implemented a multi-level security model including **Aadhaar-based employer verification** and **Facial Recognition** (using InsightFace's Buffalo L model) for test-takers to prevent impersonation.
4.  **Automatic Feedback Loop**: Established a system where resumes and profiles are automatically updated upon successful validation of skills through competency tests.

---

## System Architecture & Modules

### 1. Resume Wizard
* **Automation**: Generates professionally designed resumes from exhaustive user inputs.
* **Live Updates**: Authenticates external certifications and automatically injects newly validated skills into the resume without manual entry.

### 2. AI-Powered Job Matching & Skill Gap Analysis
* **NLP Preprocessing**: Uses tokenization, lemmatization, and skill ontologies (e.g., mapping "React.js" to "React") to normalize data.
* **Similarity Engine**: Computes **Cosine Similarity** between high-dimensional embeddings of user profiles ($P$) and job datasets ($J$).
* **Weighting Factors**:
    * $w1$: Verified Skills
    * $w2$: Certifications
    * $w3$: Experience
    * $w4$: Industry Demand Factor

### 3. Interactive Competency Testing
* **Practical Assessment**: Objective evaluation through workplace-scenario tests rather than simple multiple-choice questions.
* **Actionable Analytics**: Provides a detailed breakdown of strengths and weaknesses, mapping failures directly to personalized upskilling roadmaps.

### 4. Project Recommendation Engine
* **Market Alignment**: Uses **News APIs** to track emerging tech trends and suggest hands-on projects that address the user's specific skill gaps.
* **AI Mentorship**: Integrated assistant provides real-time debugging and code optimization tips during project execution.

---

## Technical Methodology (The Matching Algorithm)
The system follows a 7-step logic for matching:
1.  **Data Acquisition**: Retrieve Profile ($P$) and Job ($J$).
2.  **Feature Vector Generation**: Encode $P$ and $J$ into high-dimensional embeddings.
3.  **Similarity Scoring**: Calculate $M = \sum (w_i \cdot \text{feature\_score}_i)$.
4.  **Gap Detection**: Identify skills in $J$ absent in $P$ above a specific demand threshold.
5.  **Categorization**: Label gaps as **Critical** (blocking eligibility) or **Recommended**.
6.  **Recommendation**: Map gaps to e-learning APIs and platform competency tests.

---

## Conclusion & Future Scope
The study concludes that AI-augmented recruitment significantly reduces mismatches between education and labor market requirements. Future iterations will focus on **Reinforcement Learning from Human Feedback (RLHF)** to refine recommendation accuracy and integrating deeper real-time labor market analytics.