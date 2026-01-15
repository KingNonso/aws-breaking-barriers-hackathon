# AWS Breaking Barriers Challenge 2026: 7-Day GenAI Hackathon Preparation Plan

## Executive Overview

This preparation plan is designed to transform you into an effective GenAI builder within 7 days (3 hours/day) before the AWS Breaking Barriers Challenge (January 13-15, 2026). The plan balances theoretical foundation with hands-on application, preparing you to build, pitch, and deploy healthcare innovation, sustainability, or social impact solutions using AWS cloud and generative AI services. You'll progress from understanding foundation models through implementing production-ready AI agents, with emphasis on rapid prototyping and demo-ready solutions.

---

## Day 1: Foundation Models & Amazon Bedrock Fundamentals

### Learning Objectives

- Understand what foundation models are and how they differ from traditional ML
- Master Amazon Bedrock service architecture and access patterns
- Explore available foundation models (Claude, Amazon Titan, Stable Diffusion)
- Build your first inference using Bedrock console and API
- Understand the AI Engineering stack and evaluation methodology

### Key Topics

1. **Foundation Models Basics**

   - What makes FMs different from traditional ML models
   - Transformer architecture and self-attention (conceptual understanding)
   - Instruction tuning and in-context learning
   - Model families: Claude 3, Titan, Cohere, Stability AI

2. **Amazon Bedrock Deep Dive**

   - Service architecture: model access, provisioning, billing
   - Available models and use-case mapping
   - Inference API fundamentals
   - Bedrock Playground vs. API access
   - Pricing models (on-demand vs. provisioned throughput)

3. **Evaluation Fundamentals**
   - Why evaluation matters for GenAI apps
   - Automatic evaluation approaches (AI-as-a-judge)
   - Setting success metrics for hackathon projects

### Hands-On Exercise: Multi-Model Comparison

1. **Setup**: Access AWS Bedrock console
2. **Task**: Create a simple healthcare scenario—"Write a patient education guide for Type 2 diabetes"
3. **Execution**:
   - Test the same prompt across 3 different models (Claude 3 Sonnet, Amazon Titan, Cohere Command)
   - Compare outputs for accuracy, tone, and length
   - Use the Bedrock Playground to experiment with temperature and max tokens
4. **Deliverable**: Screenshot comparison table showing model strengths/weaknesses for healthcare use case

### Book Reading Schedule

- **AI Engineering** (Chip Huyen): Chapters 1-2
  - Chapter 1: Introduction to Building AI Applications with Foundation Models
  - Chapter 2: Understanding Foundation Models (pp. 49-100)
  - Focus: Skim Transformer architecture; deep dive into foundation model capabilities and limitations
- **Building LLM Powered Applications** (Valentina Alto): Chapter 1 (Introduction to LLMs)
  - Understanding LLM fundamentals and capabilities

### Curated Resources

- **Free**: [Amazon Bedrock Official Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/) - Core reference
- **Free**: [Bedrock Flows - Visual AI Workflow Builder](https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html) - Key for hackathon rapid prototyping
- **Free**: [YouTube: Amazon Bedrock Tutorial - Crash Course](https://www.youtube.com/watch?v=8nPd3H4kcmQ) - 14-minute hands-on walkthrough
- **Free**: [Coursera: Amazon Bedrock - Getting Started](https://www.coursera.org/learn/amazon-bedrock-getting-started) - Conceptual foundation (2 hours)
- **Free**: [DataCamp: Amazon Bedrock Complete Guide](https://www.datacamp.com/tutorial/aws-bedrock) - Step-by-step setup
- **Free**: [AWS AI/ML Landscape 2026 Simplified Guide](https://dev.to/aws-builders/the-aws-aiml-landscape-in-2026-simplified-17i3) - Modern context on Bedrock's role

### 3-Hour Schedule

- 0:00-0:45 — Watch Bedrock crash course YouTube video
- 0:45-1:30 — Read AI Engineering Ch. 1-2 (skim, extract key concepts)
- 1:30-2:15 — Hands-on: Set up AWS account, access Bedrock console, test 3 models
- 2:15-3:00 — Complete deliverable comparison table + document learnings

---

## Day 2: Prompt Engineering & RAG (Retrieval-Augmented Generation)

### Learning Objectives

- Master prompt engineering techniques for deterministic outputs
- Understand RAG architecture and when to use it
- Build a simple knowledge-based system (healthcare/sustainability use case)
- Implement source citation and fact-checking
- Design prompts for social impact solutions

### Key Topics

1. **Prompt Engineering Best Practices**

   - Anatomy of effective prompts (instruction, context, examples, constraints)
   - Few-shot vs. zero-shot prompting
   - Chain-of-thought (CoT) reasoning for complex tasks
   - Output schema enforcement (structured outputs)
   - Prompt injection risks and mitigation

2. **RAG Architecture**

   - When RAG is necessary (knowledge cutoff, proprietary data, accuracy)
   - Data ingestion pipeline: chunking strategies, embeddings
   - Vector databases and similarity search
   - Retrieval-augmented generation workflow
   - Ranking and re-ranking for quality

3. **Social Impact Application Patterns**
   - Healthcare: Evidence-based clinical guidance
   - Sustainability: Carbon data aggregation and reporting
   - Community: Resource navigation and service discovery

### Hands-On Exercise: RAG Healthcare Assistant

1. **Setup**: Create S3 bucket and upload sample healthcare documents
   - Use 3-5 simplified clinical guidelines (text files) on a specific condition (e.g., hypertension management)
   - Create Bedrock Knowledge Base connected to S3
2. **Task**: Build a chatbot that answers patient education questions with source citations
3. **Execution**:
   - Configure Bedrock Knowledge Base with automatic chunking (1024-token chunks)
   - Test retrieval quality with healthcare-specific queries
   - Implement prompt that cites sources in responses
   - A/B test: standard retrieval vs. metadata filtering by condition type
4. **Deliverable**:
   - Video walkthrough (2 min) of your RAG system answering 3 healthcare questions
   - Document showing retrieved sources and answer quality

### Book Reading Schedule

- **AI Engineering** (Chip Huyen): Chapter 5-6
  - Chapter 5: Prompt Engineering (pp. 175-250) — Deep dive
  - Chapter 6: RAG and Agents (pp. 251-320) — Core for hackathon
- **Building LLM Powered Applications** (Valentina Alto): Chapter 3-4
  - Focus on practical RAG implementation patterns

### Curated Resources

- **Free**: [Bedrock Knowledge Bases Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) - Step-by-step guide
- **Free**: [AWS GenAI on Bedrock Use Cases](https://www.softwareone.com/en/blog/articles/2024/03/20/generative-ai-on-amazon-bedrock-use-cases-getting-started) - Real-world patterns
- **Free**: [RAG and Agents Deep Dive](https://dev.to/aws-builders/the-aws-aiml-landscape-in-2026-simplified-17i3#agents-for-amazon-bedrock) - Architecture patterns
- **Free**: [Prompt Engineering Best Practices](https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md) - From AI Engineering author
- **Free**: [Healthcare GenAI Chatbot Patterns](https://digitalya.co/blog/using-genai-chatbots-for-hcp-portals/) - Domain-specific applications
- **Free**: [Retrieval-Augmented Generation for Healthcare](https://www.healthily.ai/post/navigating-the-hazards-of-generative-ai-health-chatbots) - Safety and accuracy considerations
- [PAID] Valentina Alto's "Building LLM Powered Applications" - Comprehensive patterns book

### 3-Hour Schedule

- 0:00-0:45 — Read AI Engineering Ch. 5-6 (focus on practical patterns)
- 0:45-1:15 — Set up S3 bucket and create Bedrock Knowledge Base
- 1:15-2:30 — Implement RAG system and test retrieval + prompting
- 2:30-3:00 — Record demo video and document sources

---

## Day 3: AWS Serverless Architecture (Lambda, API Gateway, DynamoDB)

### Learning Objectives

- Design serverless REST APIs with Lambda and API Gateway
- Implement data persistence with DynamoDB
- Build scalable backend for AI applications
- Understand concurrency, cold starts, and performance optimization
- Deploy infrastructure as code (IaC) patterns

### Key Topics

1. **AWS Lambda Fundamentals**

   - Handler functions and execution environment
   - Memory and timeout configuration (cost-performance tradeoff)
   - Cold starts and warm container reuse
   - Environment variables and secrets management
   - IAM roles and least-privilege permissions
   - Concurrency and throttling

2. **API Gateway for GenAI Backends**

   - REST vs. HTTP APIs
   - Lambda proxy integration
   - Request/response mapping and validation
   - CORS, rate limiting, API keys
   - Authentication/authorization patterns

3. **DynamoDB for AI Applications**

   - Partition keys and sorting strategies
   - On-demand vs. provisioned capacity
   - Document model for semi-structured data (conversation history, metadata)
   - Global secondary indexes for flexible querying
   - TTL for automatic cleanup

4. **Serverless Best Practices**
   - Stateless function design
   - External state management (S3, DynamoDB)
   - Error handling and retries
   - Observability: CloudWatch logs, X-Ray tracing
   - Security: encryption, VPC, environment isolation

### Hands-On Exercise: AI Chatbot Backend API

1. **Setup**: Create Lambda execution role with minimal permissions
2. **Task**: Build a REST API that serves a Bedrock-powered chatbot with conversation history
3. **Execution**:
   - Lambda function (Python/Node.js) that calls Bedrock API
   - Accepts: `POST /chat` with `{ "userId": "...", "message": "..." }`
   - Returns: `{ "response": "...", "conversationId": "...", "sourceDocuments": [...] }`
   - DynamoDB table to store conversation history (userId + timestamp)
   - API Gateway routing with request validation
   - Error handling for Bedrock API limits and timeouts
4. **Deliverable**:
   - Deployment script (SAM or CDK) to recreate infrastructure
   - Documentation of API schema and example requests/responses
   - Performance metrics: cold start time, latency, cost estimate

### Book Reading Schedule

- **AI Engineering** (Chip Huyen): Chapter 9 (pp. 400-450) — Inference optimization
- Architecture-focused: AWS Well-Architected Framework (Serverless Lens)

### Curated Resources

- **Free**: [AWS Lambda Official Tutorial](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html) - DynamoDB integration
- **Free**: [Lambda with API Gateway - REST API Tutorial](https://blog.tericcabrel.com/rest-api-aws-lambda-api-gateway-cdk/) - CDK example with MongoDB (adaptable to DynamoDB)
- **Free**: [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html) - Official AWS guide
- **Free**: [Lambda Security Best Practices](https://www.ranthebuilder.cloud/post/14-aws-lambda-security-best-practices-for-building-secure-serverless-applications) - Production hardening
- **Free**: [AWS Lambda Fundamentals for Scalability](https://dev.to/urielbitton/aws-lambda-best-practices-for-performant-scalable-serverless-functions-3ccp) - Performance tuning
- **Free**: [Top 10 Lambda Best Practices](https://lumigo.io/learn/top-10-aws-lambda-best-practices/) - Operational checklist
- **Free**: [AWS Lambda PowerTools](https://blog.localstack.cloud/serverless-best-practices-with-powertools/) - Idempotency, logging, structured data
- **Free**: [DynamoDB with S3 Access via IAM](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security_iam_service-with-iam.html) - IAM patterns

### 3-Hour Schedule

- 0:00-0:45 — Read Lambda best practices and API Gateway patterns
- 0:45-1:30 — Create Lambda function skeleton, API Gateway REST API, DynamoDB schema
- 1:30-2:30 — Implement Bedrock API calls, conversation history, error handling
- 2:30-3:00 — Write deployment script (SAM) and document API schema

---

## Day 4: Amazon SageMaker Essentials & Quick ML Model Deployment

### Learning Objectives

- Understand SageMaker Studio and notebook environments
- Use SageMaker for data preparation and feature engineering
- Deploy pre-trained models as endpoints
- Understand built-in algorithms (XGBoost, Linear Learner)
- Integrate SageMaker models into Bedrock workflows

### Key Topics

1. **SageMaker Studio Overview**

   - Notebook instances and SageMaker Studio IDE
   - Pre-built environments and kernel management
   - Data access: S3, local upload, external sources
   - Marketplace models and community code

2. **Data Preparation & Feature Engineering**

   - SageMaker Data Wrangler for ETL
   - Built-in processing jobs (Spark, Python containers)
   - Feature Store for ML feature management
   - Handling healthcare data (HIPAA considerations), sustainability metrics

3. **Training & Deployment**

   - Built-in algorithm containers (no custom code needed)
   - Training job management and monitoring
   - Model registry and versioning
   - Real-time endpoints vs. batch transform
   - Cost estimation and optimization

4. **SageMaker + Bedrock Integration**
   - Using trained models as Lambda functions (inference)
   - Feature embedding generation for similarity search
   - Custom model serving via SageMaker endpoints called by Lambda

### Hands-On Exercise: Sustainability Metrics Prediction Model

1. **Setup**: Download sample environmental data (e.g., carbon footprint dataset)
2. **Task**: Train a simple regression model to predict carbon emissions based on business metrics
3. **Execution**:
   - Use SageMaker notebook to load and explore data
   - Create 3-5 features (energy consumption, waste, travel distance)
   - Train XGBoost model using SageMaker built-in container
   - Deploy as SageMaker endpoint
   - Create Lambda function to invoke endpoint
   - Integrate prediction into chatbot (e.g., "Based on your metrics, estimated CO2 is...")
4. **Deliverable**:
   - Jupyter notebook with complete training pipeline
   - Model performance metrics (RMSE, R²)
   - Lambda code calling SageMaker endpoint
   - Cost analysis for the endpoint

### Book Reading Schedule

- **AI Engineering** (Chip Huyen): Chapter 7-8 (pp. 325-400)
  - Chapter 7: Fine-tuning (brief, for context)
  - Chapter 8: Dataset Engineering (critical for sustainability/healthcare data)

### Curated Resources

- **Free**: [SageMaker Examples Repository](https://github.com/aws/amazon-sagemaker-examples) - Official code samples
- **Free**: [SageMaker End-to-End Workshop](https://github.com/aws-samples/sagemaker-end-to-end-workshop) - Churn prediction walkthrough (adaptable)
- **Free**: [SageMaker Project Ideas](https://www.projectpro.io/article/amazon-sagemaker-projects-examples-and-ideas/628) - 10 beginner-friendly templates
- **Free**: [SageMaker Hands-On Tutorial](https://www.youtube.com/watch?v=M5tFyhdNj40) - YouTube overview
- **Free**: [SageMaker Overview for Beginners](https://www.bmc.com/blogs/amazon-sagemaker/) - Conceptual introduction with examples
- **Free**: [SageMaker Training Compiler Examples](https://docs.aws.amazon.com/sagemaker/latest/dg/training-compiler-examples-and-blogs.html) - Performance optimization
- **Free**: [AWS Sustainability Insights Framework on SageMaker](https://aws.amazon.com/solutions/guidance/sustainability-insights-framework-on-aws/) - Sustainability use case architecture

### 3-Hour Schedule

- 0:00-0:45 — Read AI Engineering Ch. 7-8 and review SageMaker examples
- 0:45-1:30 — Set up SageMaker notebook, load data, EDA and feature engineering
- 1:30-2:30 — Train model, deploy endpoint, test predictions
- 2:30-3:00 — Write Lambda integration code and document results

---

## Day 5: Amazon Q Developer & AI-Assisted Development

### Learning Objectives

- Leverage Amazon Q for rapid code generation
- Use Q Developer for code refactoring and documentation
- Understand Q's architecture and model capabilities
- Optimize developer workflow for 72-hour hackathon
- Implement secure coding patterns with Q assistance

### Key Topics

1. **Amazon Q Developer Capabilities**

   - Inline chat in VS Code and JetBrains IDEs
   - Code generation from natural language
   - Code refactoring and optimization
   - Test generation and documentation
   - Git integration and commit message generation

2. **Q Developer for AI Engineering**

   - Prompt engineering for better code generation
   - Multi-language support (Python, JavaScript, TypeScript, Java)
   - Integration with AWS SDKs and Bedrock APIs
   - Security-aware code generation

3. **Hackathon-Optimized Workflow**

   - Rapid scaffolding of serverless applications
   - IaC generation (CloudFormation, CDK)
   - API endpoint boilerplate
   - Error handling and logging templates
   - Testing and validation helpers

4. **Best Practices for Production**
   - Code review process with Q suggestions
   - Avoiding common pitfalls (hardcoded secrets, insecure permissions)
   - Performance optimization suggestions
   - Cost-aware code patterns

### Hands-On Exercise: Rapid Service Scaffolding

1. **Setup**: Install Amazon Q in your IDE (VS Code or JetBrains)
2. **Task**: Use Q to generate a complete healthcare appointment scheduling API
3. **Execution**:
   - Prompt Q: "Generate a Python Lambda function that handles appointment scheduling with validation and DynamoDB persistence"
   - Review generated code, iterate with follow-up prompts
   - Use Q to add error handling: "Add comprehensive error handling with logging"
   - Generate tests: "Write pytest tests for the appointment scheduling function"
   - Generate documentation: "Add docstrings and API documentation in OpenAPI format"
   - Generate IaC: "Create AWS CDK code to deploy this Lambda + API Gateway + DynamoDB"
4. **Deliverable**:
   - Complete working code for microservice (Lambda function + CDK)
   - Test suite with >80% code coverage
   - OpenAPI specification
   - Time tracking: total time from prompt to deployment

### Book Reading Schedule

- **AI Engineering** (Chip Huyen): Chapter 10 (pp. 475-525) — Architecture and integration patterns
- Focus: Understanding how to evaluate and integrate AI models into applications

### Curated Resources

- **Free**: [Amazon Q Developer Official Page](https://aws.amazon.com/q/developer/) - Feature overview and pricing
- **Free**: [Using Amazon Q as Coding Assistant](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/use-q-developer-as-coding-assistant-to-increase-productivity.html) - Best practices guide
- **Free**: [Amazon Q Developer Capabilities Deep Dive](https://venturebeat.com/ai/aws-launches-in-line-q-developer-ai-coding-assistant-to-take-on-microsofts-github-copilot) - Feature comparison and use cases
- **Free**: [Amazon Q IDE Integration Guide](https://aws.amazon.com/q/developer/) - Setup and first steps
- **Free**: [YouTube: Amazon Q Developer Walkthrough](https://www.youtube.com/results?search_query=amazon+q+developer+tutorial) - Video demos

### 3-Hour Schedule

- 0:00-0:30 — Install Amazon Q, familiarize with IDE integration
- 0:30-1:00 — Read AI Engineering Ch. 10 (architecture patterns)
- 1:00-2:30 — Use Q to generate appointment scheduling API (function + CDK + tests)
- 2:30-3:00 — Review generated code, iterate, document learnings

---

## Day 6: IAM, S3, Cloud Security & Essential AWS Services

### Learning Objectives

- Design secure IAM policies following least-privilege principle
- Implement S3 bucket security and data lifecycle management
- Understand encryption (at-rest and in-transit)
- Set up secure credential management for AI applications
- Prepare infrastructure for healthcare/sensitive data handling

### Key Topics

1. **IAM Best Practices**

   - Principal, Action, Resource, Condition framework
   - Least-privilege policies: granular permissions
   - Service roles for Lambda, SageMaker, Bedrock
   - Resource-based vs. identity-based policies
   - Cross-account access patterns (for multi-org hackathons)

2. **S3 Security & Data Management**

   - Bucket policies and ACLs (access control)
   - Encryption: SSE-S3, SSE-KMS, client-side
   - Versioning and lifecycle policies
   - Data retention and compliance (healthcare HIPAA, sustainability audits)
   - Access logging and CloudTrail integration

3. **Secrets Management**

   - AWS Secrets Manager for API keys, database credentials
   - Parameter Store for configuration
   - Environment variables vs. secrets (best practices)
   - Rotation strategies

4. **Healthcare & Sensitive Data Considerations**

   - De-identification and anonymization patterns
   - HIPAA compliance basics (encryption, access logs, audit trails)
   - Data residency requirements
   - PII (personally identifiable information) redaction in logs

5. **Networking & Compliance**
   - VPC basics for private Lambda execution
   - Security groups and network ACLs
   - API Gateway authentication (API keys, OAuth)
   - DDoS protection (AWS Shield, WAF for public APIs)

### Hands-On Exercise: Secure Healthcare Data Pipeline

1. **Setup**: Create S3 bucket with strict security controls
2. **Task**: Build secure data ingestion pipeline for healthcare records
3. **Execution**:
   - Create S3 bucket with versioning, encryption (SSE-KMS), lifecycle policy
   - Configure bucket policy: allow only specific Lambda role to read, deny all public access
   - Create IAM role for Lambda with minimal permissions:
     - `s3:GetObject` on specific prefix (e.g., `healthdata/*`)
     - `bedrock:InvokeModel` for inference only
     - `dynamodb:PutItem` to store results
   - Implement de-identification logic in Lambda (hash or mask sensitive fields)
   - Set up CloudTrail logging for all S3 access
   - Test: verify unauthorized access is blocked
4. **Deliverable**:
   - IAM policy JSON file with detailed comments
   - S3 bucket configuration template
   - Lambda function demonstrating secure data handling
   - Security checklist for hackathon deployment

### Book Reading Schedule

- Supplement with AWS IAM documentation and security whitepapers
- **Focus areas**: Least-privilege policies, secret management, audit logging

### Curated Resources

- **Free**: [AWS IAM Best Practices](https://spacelift.io/blog/iam-policy) - Visual editor walkthrough
- **Free**: [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html) - Official AWS guide
- **Free**: [S3 + IAM Integration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security_iam_service-with-iam.html) - Policy examples
- **Free**: [IAM Policy Examples for S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Integrating.Authorizing.IAM.S3CreatePolicy.html) - Detailed walkthrough
- **Free**: [Lambda Security Best Practices](https://www.ranthebuilder.cloud/post/14-aws-lambda-security-best-practices-for-building-secure-serverless-applications) - Production hardening
- **Free**: [AWS Well-Architected Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/) - Strategic guide
- **Free**: [Healthcare GenAI Security Considerations](https://www.healthily.ai/post/navigating-the-hazards-of-generative-ai-health-chatbots) - Domain-specific concerns

### 3-Hour Schedule

- 0:00-0:45 — Read IAM/S3 best practices and healthcare compliance notes
- 0:45-1:30 — Create S3 bucket, configure encryption, lifecycle, bucket policy
- 1:30-2:30 — Write IAM policy, create Lambda role, implement data de-identification
- 2:30-3:00 — Test security controls, document configuration, create checklist

---

## Day 7: Hackathon Strategy, Architecture Design & Demo Preparation

### Learning Objectives

- Apply TOGAF ADM principles to rapidly scope social impact solution
- Design hackathon-ready solution architecture (72-hour constraint)
- Master idea scoping for social impact projects
- Prepare compelling demos and pitch narratives
- Understand team dynamics and collaboration patterns

### Key Topics

1. **Rapid Architecture Design (Hackathon Context)**

   - Trade-offs: MVP vs. production-grade (choose MVP)
   - Monolithic vs. microservices (stay simple for 72 hours)
   - Critical path: identify must-have features vs. nice-to-have
   - Technology selection: leverage managed services (Bedrock, SageMaker, Lambda)
   - Risk identification: what could break your demo?

2. **TOGAF ADM Applied to Hackathon (Simplified)**

   - **Phase A: Architecture Vision** (Day 1)
     - Define business context: which social problem are you solving?
     - Identify stakeholders: charity, users, judges, team
     - Document constraints: 72 hours, AWS budget, team skills
     - Create vision statement: "Enable charities to serve X more people by reducing Y hours of manual work"
   - **Phase B: Business Architecture** (Day 1)
     - Map charity processes: current state (inefficient) vs. target state (with your solution)
     - Identify key value drivers: cost savings, reach expansion, quality improvement
   - **Phase C/D: Information & Technology Architecture** (Day 2)
     - Design data flows: where does data come from? How is it processed?
     - Select technologies: Bedrock for NLP, SageMaker for predictions, Lambda for automation
   - **Phase E: Opportunities & Solutions** (Day 2)
     - Define implementation projects: phased rollout (not needed for hackathon, but good to mention)
     - Calculate impact metrics: lives touched, hours saved, cost reduction
   - **Note**: For hackathon, compress to 48-hour cycle (A-B-C/D collapsed into Day 1 scoping)

3. **Idea Scoping Framework for Social Impact (Hackathon Version)**

   - **What change are you trying to create?**
     - Start specific, not vague: "Reduce administrative burden on nurses by 2 hours/day" vs. "improve healthcare"
     - Quantify impact: lives affected, resources saved, quality improvement
   - **Who are you designing for?**
     - Primary users: charity staff, end beneficiaries, or both?
     - Secondary stakeholders: volunteers, donors, regulatory bodies
     - Personas: Create 2-3 realistic user personas (name, pain point, goal)
   - **What do you know vs. what do you need to learn?**
     - Assumptions: What are you assuming about the charity's problem? About technology?
     - Validation: Which assumptions can you test with the charity team on Day 1?
     - Pivot triggers: What evidence would cause you to change direction?
   - **Solution constraints**
     - Budget: AWS free tier or allocated credits?
     - Time: 72 hours for what MVP?
     - Technical constraints: team skills, Bedrock model availability
     - Deployment: working prototype, beta testing, or production-ready?

4. **Architectural Clarifying Questions for Social Impact Projects**

   - **Problem Understanding**
     - What is the charity currently doing manually that is time-consuming or error-prone?
     - How many people does this process affect monthly? What's the cost?
     - Why hasn't this been solved with traditional software?
   - **GenAI-Specific Questions**
     - Is NLP/LLM the right tool? (Could rule-based logic be simpler?)
     - What data will feed the model? Is it clean, labeled, and accessible?
     - How will you handle model failures? What's the fallback?
     - What are the failure modes? (Hallucinations, bias, privacy risks)
   - **Sustainability & Scalability**
     - Can the solution scale to 10x more users without infrastructure changes?
     - What are the ongoing costs (Bedrock API, SageMaker endpoints)?
     - Can the charity maintain this after the hackathon without your team?
   - **Compliance & Ethics**
     - Are there regulatory requirements (HIPAA, GDPR, accessibility)?
     - How will you ensure fairness across different populations?
     - What happens to data after the hackathon? (Deletion, licensing)

5. **Business Model & Impact Articulation**

   - **Impact Metrics Dashboard**
     - Lives Touched: Direct beneficiaries impacted
     - Resources Saved: Time, money, energy (quantify in hours, currency, CO2)
     - Quality Improvements: Accuracy, coverage, accessibility gains
     - Efficiency Gains: Process bottleneck reduction
   - **Sustainability**
     - Operational cost per user after launch
     - Revenue model (if applicable): grants, donations, freemium
     - Growth trajectory: pilot to scale plan

6. **Demo Preparation for Judges**

   - **Structure** (3-5 minutes max)
     - Problem statement (30 sec): "Charities waste 100+ hours/month on X"
     - Your solution (30 sec): "We built an AI assistant that does X, saving 80 hours/month"
     - Live demo (2-3 min): Show the working product, real scenario
     - Impact & metrics (30 sec): "This enables us to serve 500 more people annually"
   - **Demo Script**
     - Prepare 3-4 interaction scenarios (best case, common case, edge case)
     - Backup screenshots/video in case live demo fails
     - Practice with your team; timing is critical
   - **Storytelling**
     - Lead with the charity's pain, not the technology
     - Show how a real person benefits (user persona + story)
     - End with vision: "This is just the start; imagine if every charity had this..."

7. **Team Collaboration Best Practices for GenAI Projects**

   - **Role Assignment**
     - **Product Owner**: Owns problem understanding, charity liaison, demo narrative
     - **Architects**: Responsible for system design, tech choices, risk mitigation
     - **Frontend/Integration**: Builds UI/chatbot interface, connects to backend
     - **Backend/ML**: Implements Bedrock integration, data pipelines, model serving
     - **DevOps/Infra**: Deployment, monitoring, cost tracking, security
   - **Daily Standup** (15 min)
     - What did each team member complete yesterday?
     - What's the blocker or risk?
     - Who needs help from whom?
   - **Knowledge Sharing**
     - Pair programming on critical components (Bedrock integration, IAM setup)
     - Document decisions and trade-offs in shared wiki/notes
     - Code reviews by 2+ people before merge (Q Developer can help here)
   - **Feedback Loops**
     - Build rapid iteration into your plan (v1 by Day 2 EOD, v2 by Day 3 morning)
     - Charity feedback loop: share prototype with charity partner ASAP
     - User testing: if time permits, test with real users (not just judges)

8. **Hackathon Execution Timeline (72-Hour Compressed)**
   - **Day 1 (Jan 13): Ignite & Design**
     - Morning: Keynotes, charity deep-dives, workshops
     - Afternoon: Team formation, charity problem exploration (1-2 hours)
     - Evening: Architecture design, tech spike, MVP scope definition
     - Deliverable: Scoped design doc (1-2 pages), tech stack decision, role assignments
   - **Day 2 (Jan 14): Build & Iterate**
     - Morning: Data ingestion setup, Bedrock/SageMaker models trained/deployed
     - Afternoon: Backend API working, frontend scaffolding
     - Evening: Integration tests, demo script rehearsal
     - Deliverable: Working API endpoint, alpha demo with dummy data
   - **Day 3 (Jan 15): Polish & Present**
     - Morning: Real data integration, error handling, demo refinement
     - Afternoon: Documentation, architecture diagram, impact calculations
     - Late afternoon: Final rehearsal, judges' Q&A prep
     - Deliverable: Live demo + pitch, codebase, architecture diagram, impact metrics

### Hands-On Exercise: Scoped Solution Design

1. **Setup**: Choose one of three charity challenges (healthcare, sustainability, community)
2. **Task**: Design a complete AI solution architecture within hackathon constraints
3. **Execution**:
   - **Problem Analysis** (30 min):
     - Articulate the charity's current process and bottleneck
     - Quantify impact: hours wasted, people underserved, money spent
     - Brainstorm 3 AI-powered solutions; select best (why?)
   - **TOGAF-Simplified Design** (60 min):
     - Vision: 1-page document with problem, solution, stakeholders, constraints
     - Business Architecture: Draw current vs. target process flow
     - Technology Architecture: System diagram (Bedrock, Lambda, API Gateway, DynamoDB, S3)
     - Data Architecture: Where does data come from? How is it transformed?
   - **Scoping & Risk** (30 min):
     - MVP scope: List features for 72-hour build (must-have vs. nice-to-have)
     - Tech debt: What are you cutting corners on? Is it acceptable?
     - Risks: What could fail? How will you mitigate?
     - Validation: What will you measure to prove impact?
   - **Demo Narrative** (30 min):
     - Write 3-minute demo script with transition points
     - Identify 2-3 failure scenarios; plan fallbacks
     - Practice with timer
4. **Deliverable**:
   - Architecture diagram (draw.io, Lucidchart, or even ASCII art)
   - Design document: problem, solution, architecture, impact metrics (2-3 pages)
   - Demo script with timing markers
   - Risk/mitigation matrix
   - Resource estimate: AWS services needed, cost, team hours

### Curated Resources

- **Free**: [TOGAF ADM Phases Overview](https://www.knowledgehut.com/blog/it-service-management/togaf-phases) - Simplified breakdown
- **Free**: [Social Impact Project Scoping Framework](https://dschool.stanford.edu/stories/project-scoping-ai-scopey-social-change) - Stanford d.school tool (Scopey)
- **Free**: [Logical Framework for Social Impact](https://www.linkedin.com/pulse/logical-framework-basic-core-social-impact-projects-enrique-rubio) - Planning structure
- **Free**: [Social Impact Assessment Steps](https://www.projectworks.com/blog/social-impact-assessment) - Evaluation methodology
- **Free**: [How to Run AI Hackathons](https://www.virtasant.com/ai-today/how-to-create-and-host-an-ai-hackathon-in-6-weeks) - Enterprise playbook
- **Free**: [Posit AI Hackathon Lessons](https://posit.co/blog/llm-hackathon-lessons-learned/) - Real project insights
- **Free**: [Torq AI Hackathon Best Practices](https://torq.io/blog/ai-hackathon/) - Team execution patterns
- **Free**: [AWS Breaking Barriers Challenge Details](https://aws.amazon.com/events/aws-breaking-barriers-challenge/) - Official event info
- **Free**: [OpenAI Hackathon Playbook](https://academy.openai.com/public/clubs/champions-ecqup/resources/hackathon-playbook-2026-09-15) - Team formation, tool access, judging

### 3-Hour Schedule

- 0:00-0:50 — Read TOGAF ADM (simplified) and social impact scoping framework
- 0:50-2:00 — Complete hands-on design exercise (architecture, narrative, risks)
- 2:00-3:00 — Practice demo script, gather feedback from peer review, refine

---

## Summary: Book Reading Schedule (Aligned to Days)

| Day | AI Engineering (Chip Huyen) | Building LLM Apps (Valentina Alto) | Focus                                   |
| --- | --------------------------- | ---------------------------------- | --------------------------------------- |
| 1   | Ch. 1-2                     | Ch. 1                              | Foundation models, Bedrock fundamentals |
| 2   | Ch. 5-6                     | Ch. 3-4                            | Prompt engineering, RAG architecture    |
| 3   | Ch. 9                       | -                                  | Inference optimization, serverless      |
| 4   | Ch. 7-8                     | -                                  | Fine-tuning, dataset engineering        |
| 5   | Ch. 10                      | -                                  | Architecture patterns, integration      |
| 6   | (AWS docs)                  | -                                  | Security, IAM, best practices           |
| 7   | (Review)                    | -                                  | Synthesis, rapid architecture design    |

**Reading Strategy**: Skim chapters for structure; deep dive on sections marked in italics. Use YouTube summaries for quick refreshers.

---

## TOGAF ADM Phases Applied to Hackathon (2-Day Compressed Cycle)

### Day 1 Morning: Phases A & B (4 hours)

- **Phase A: Architecture Vision**
  - Read charity brief and problem statement
  - Identify business context, stakeholders, constraints
  - Create vision: "Enable [charity] to [benefit] by [solution]"
  - Document scope: 72-hour MVP, AWS services, team skills
- **Phase B: Business Architecture**
  - Map current process (interview charity contact)
  - Identify bottlenecks and pain points
  - Design target process (how AI solution changes workflow)
  - Quantify impact: time saved, reach expanded, cost reduced

### Day 1 Afternoon: Phases C & D (4 hours)

- **Phase C: Information Systems Architecture**
  - Data flow diagram: sources (charity database, external APIs) → processing → outputs
  - Identify data models: conversation logs, user profiles, transaction records
  - Security/compliance: PII handling, encryption, audit trails
- **Phase D: Technology Architecture**
  - Service selection: Bedrock (LLM), Lambda (compute), API Gateway (interface), DynamoDB (storage)
  - Deployment model: serverless (AWS Lambda), managed services (no ops overhead)
  - Integration points: How does AI plug into existing charity systems?

### Day 2: Phases E & (abbreviated) F (4 hours)

- **Phase E: Opportunities & Solutions**
  - Feature prioritization: MVP scope (Day 2-3), Future work (post-hackathon)
  - Solution options: Rule-based vs. AI, in-house vs. outsourced (not applicable for hackathon)
- **Phase F: Migration Planning** (Abbreviated)
  - Pilot approach: Demo to charity team, gather feedback
  - Success metrics: number of interactions, user satisfaction, time savings

---

## Idea Scoping Framework: Hackathon Edition

Use the **Stanford d.school Scopey framework** (adapted for 72-hour hackathon):

### 1. **What Change Are You Trying to Create?**

- Avoid: "Build an AI chatbot"
- Target: "Reduce nurse administrative time by 2 hours/day through intelligent appointment scheduling"
- Quantify: 100 nurses × 2 hours/day × 250 working days = 50,000 hours/year saved = $2.5M value

### 2. **Who Are You Designing For?**

- Primary: Overworked nurses, clinic schedulers, patients needing appointments
- Secondary: Hospital administrators (cost tracking), auditors (compliance)
- Create personas:
  - **Sarah, Nurse Manager**: "I spend 4 hours/day scheduling while patients wait 2+ weeks. I want to reduce wait times to <3 days and free up time for patient care."
  - **Marcus, Clinic Patient**: "I can't reach the clinic during business hours. I want to book appointments via chat, anytime."

### 3. **What Do You Know vs. Need to Learn?**

- **Know**: Clinic scheduling is manual, causes delays, frustrates staff and patients
- **Assumptions**:
  - Patient no-show rate is 20% (find real number!)
  - Nurses spend 30% of their time on admin (validate with interviews!)
  - An AI chatbot can handle 80% of appointment requests (test this!)
- **Learn**: On Day 1, interview clinic staff—what's the real bottleneck?

### 4. **Solution Constraints & Scope**

- **Budget**: $500 AWS credits for hackathon (pace your Bedrock API calls!)
- **Time**: 72 hours total; plan 12 hours for sleep, leaving 60 hours of work
- **MVP**: Chatbot that books appointments + reschedules existing ones
- **Nice-to-have** (cut if time-pressed): Automated no-show prediction, patient SMS reminders

### 5. **Validation Plan**

- **Day 1 Eve**: Demo v0 (proof of concept) to clinic contact
- **Day 2 Afternoon**: v1 (working with real clinic data) feedback session
- **Day 3 Morning**: Final refinement based on feedback
- **Success metric**: Clinic staff rates solution 4/5+ for usability; handles 10+ test appointments correctly

---

## Architectural Clarifying Questions: Template

**Fill this out on Day 1 with your team and charity partner:**

### Problem Understanding

- [ ] What is the most time-consuming process you want to automate?
- [ ] How many staff-hours are spent on this weekly?
- [ ] What percentage of cases could AI handle safely (vs. require human review)?
- [ ] What are the failure modes? (Wrong appointment time, incorrect patient match, privacy breach)

### GenAI Fit

- [ ] Is natural language processing the right tool? (Could you use simpler rule-based logic?)
- [ ] What data sources will feed the AI? (Are they clean, labeled, accessible, permissioned?)
- [ ] What's your hallucination tolerance? (Is 5% wrong output acceptable?)
- [ ] How will users know when the AI is uncertain and should escalate to humans?

### Data & Privacy

- [ ] What patient/staff data will the solution touch? (Names, medical history, phone numbers)
- [ ] Are there regulatory requirements? (HIPAA for healthcare, GDPR if EU data involved)
- [ ] How will you prevent models from remembering sensitive information?
- [ ] What happens to data after the hackathon? (Deletion, licensing, retention)

### Deployment & Sustainability

- [ ] Can the charity run this themselves after the hackathon, or does it need your team?
- [ ] What's the monthly cost? (Bedrock API, Lambda compute, storage)
- [ ] Who will monitor the system? (Uptime, model quality, user satisfaction)
- [ ] How often does the model need retraining? (Monthly, yearly, never)

### Success Metrics

- [ ] What's the primary metric? (Time saved, reach expanded, quality improved)
- [ ] How will you measure it? (User surveys, time logs, transaction counts)
- [ ] What's the target? (Save 1 hour/day, serve 100 more patients, reduce errors by 50%)
- [ ] When will you measure? (Launch + 1 month, 3 months post-hackathon)

---

## Demo Preparation Checklist (Last 48 Hours)

### Demo Script (3-5 Minutes)

- [ ] **Opening** (30 sec): Lead with the charity's pain, not the tech
  - _Example_: "Nurses spend 4 hours/day on admin. Patients wait 2+ weeks for appointments. This is broken."
- [ ] **Solution** (30 sec): What you built, in plain language
  - _Example_: "We built an AI chatbot that books appointments, handles rescheduling, and checks insurance. Nurses spend 30 minutes on scheduling instead of 4 hours."
- [ ] **Live Demo** (2-3 min): Show real scenario
  - User interaction: "Hi, I need an appointment next week" → Chatbot books it
  - Show one edge case: "What if the patient is already in the system?" (redirect to reschedule)
  - Fallback scenario: "If the chatbot is unsure, it escalates to a human"
- [ ] **Impact** (30 sec): Quantify the benefit
  - _Example_: "This enables us to serve 500 more patients annually and free up 50,000 nursing hours/year for patient care"
- [ ] **Close**: Vision beyond hackathon
  - _Example_: "Imagine every clinic having this. Together, we could recover 5 million hours of healthcare worker time globally."

### Live Demo Preparation

- [ ] Test demo environment end-to-end (internet, API, database)
- [ ] Prepare 3-4 demo scenarios (happy path, alternate path, error handling)
- [ ] Have screenshots/video backup (if live demo fails, you can switch)
- [ ] Dry run: practice with your team 5+ times with timer
- [ ] Identify single point of failures: cold Lambda start? Bedrock latency? Plan mitigations

### Presentation Materials

- [ ] Architecture diagram: clear, labeled, printed as backup
- [ ] 1-slide impact dashboard: metrics, lives touched, resources saved
- [ ] Pitch deck: 5-7 slides (problem, solution, demo, impact, team, next steps)
- [ ] Code repository: GitHub link, README with setup instructions
- [ ] Technical documentation: API spec, deployment guide, architecture decisions

### Judges' Q&A Prep

- [ ] **Technical depth**: Be ready to explain Bedrock, RAG, Lambda architecture
- [ ] **Business impact**: Have specific numbers (time saved, people reached, cost)
- [ ] **Sustainability**: Can the charity run this? What's the ongoing cost?
- [ ] **Risks**: What can go wrong? How did you mitigate?
- [ ] **Realism**: Be honest about what's MVP vs. future work
- [ ] **Learning**: What would you do differently if you had more time?

### Post-Hackathon (If You Win)

- [ ] AWS support contact for deployment to production
- [ ] Charity partnership plan: ongoing development, user training
- [ ] Open-source strategy: will you release code? Under which license?
- [ ] Scalability plan: from single clinic to network of clinics
- [ ] Funding/grants: identify sources for further development

---

## Team Collaboration Best Practices for GenAI Projects

### Role Definitions (Adjust to Team Size)

1. **Product Owner / Charity Liaison**

   - Owns problem understanding and charity relationship
   - Writes user stories, sets MVP scope
   - Presents demo and pitch

2. **Architect / Lead Developer**

   - Tech stack decisions: Bedrock vs. SageMaker, REST vs. gRPC
   - System design: data flows, API schemas, error handling
   - Code review and technical quality

3. **AI/ML Engineer**

   - Bedrock integration: prompt engineering, model selection
   - RAG setup: data ingestion, retrieval optimization
   - Evaluation: test queries, metrics, iteration

4. **Backend Engineer**

   - Lambda development: API endpoints, database operations
   - Integrations: Bedrock API calls, error handling
   - Testing: unit tests, integration tests

5. **Frontend/Full-Stack Engineer** (if building UI)

   - Chatbot interface: web, mobile, or Slack bot
   - User experience: clear error messages, help text
   - Accessibility: WCAG compliance if healthcare/social impact

6. **DevOps/Infrastructure**
   - Deployment: SAM/CDK scripts, CI/CD setup
   - Monitoring: CloudWatch dashboards, error alerts
   - Security: IAM roles, encryption, audit logging

### Daily Standups (15 Minutes)

```
Format:
- [Name]: Completed [X yesterday], today working on [Y], blocker is [Z?]
- Example: "Completed Bedrock integration, today building Lambda wrapper, need help with SageMaker cold start"
```

### Decision Log

Keep a shared document of critical decisions:

```
[Decision]: Use Claude 3 Sonnet for chatbot (vs. Titan or Cohere)
[Rationale]: Better instruction following, faster inference, lower cost
[Date]: Jan 13, 10 AM
[Owner]: AI Lead
[Alternatives Considered]: Cohere Command, Amazon Titan (both slower)
[Risk]: Billing surprises if throughput exceeds projections
[Mitigation]: Set Bedrock quota limit, monitor usage daily
```

### Code Review Checklist (Use Amazon Q to Speed Up)

- [ ] Does the code follow security best practices? (No hardcoded secrets, IAM least privilege)
- [ ] Is error handling comprehensive? (Try/catch, logging, user-facing messages)
- [ ] Are tests passing? (Unit tests, integration tests)
- [ ] Is it documented? (Docstrings, README, API schema)
- [ ] Is it performant? (No N+1 queries, reasonable Lambda memory)
- [ ] Is it cost-aware? (Efficient Bedrock calls, DynamoDB on-demand sizing)

### Feedback Loops (Iterate Daily)

- **v0 (End of Day 1)**: Proof of concept (Bedrock + Lambda working, tested locally)
- **v1 (Afternoon Day 2)**: Working with real data (API + DynamoDB + UI scaffold)
- **v2 (Morning Day 3)**: Polished and tested (error handling, demo-ready, documented)

---

## Conclusion: Your Competitive Advantage for AWS Breaking Barriers Challenge

By Day 7, you'll have:

1. **Technical Foundation**: Mastery of Bedrock, Lambda, SageMaker, and serverless architecture
2. **AI Engineering Skills**: Prompt engineering, RAG, evaluation, production deployment
3. **Hackathon Strategy**: Rapid scoping, TOGAF-guided design, team collaboration
4. **Demo Readiness**: Clear problem framing, working prototype, compelling narrative
5. **Infrastructure**: Secure, scalable, cost-effective AWS solution architecture
6. **Leadership Ability**: Guide your team through ambiguity and deliver under pressure

**Remember**: In a 72-hour hackathon, **simplicity beats perfection**. A working MVP that solves a real charity problem, well-presented, will beat a half-finished sophisticated system every time. Use the first 2 days to build. Use Day 3 to polish and present.

**Good luck at the AWS Breaking Barriers Challenge! 🚀**

---

## Appendix: Quick Reference Cheat Sheets

### Bedrock API Snippet (Python)

```python
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

response = client.invoke_model(
    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    body=json.dumps({
        'anthropic_version': 'bedrock-2026-06-01',
        'max_tokens': 1024,
        'messages': [
            {'role': 'user', 'content': 'Schedule an appointment for diabetes care'}
        ]
    })
)

print(json.loads(response['body'].read())['content'][0]['text'])
```

### Lambda + API Gateway Skeleton (TypeScript)

```typescript
import { APIGatewayProxyHandler } from "aws-lambda";
import { invokeBedrockModel } from "./bedrock-client";

export const handler: APIGatewayProxyHandler = async (event) => {
  try {
    const body = JSON.parse(event.body || "{}");
    const response = await invokeBedrockModel(body.userMessage);
    return {
      statusCode: 200,
      body: JSON.stringify({ message: response }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};
```

### DynamoDB IAM Policy (Minimal)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["dynamodb:PutItem", "dynamodb:GetItem"],
      "Resource": "arn:aws:dynamodb:us-east-1:ACCOUNT:table/ChatHistory"
    }
  ]
}
```

### SAM Deployment (CloudFormation Infrastructure as Code)

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Resources:
  ChatFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: dist/handler.handler
      Runtime: nodejs18.x
      Environment:
        Variables:
          BEDROCK_MODEL: anthropic.claude-3-sonnet-20240229-v1:0
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref ChatTable
        - Statement:
            - Effect: Allow
              Action: bedrock:InvokeModel
              Resource: "*"

  ChatTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: ChatHistory
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: userId
          AttributeType: S
      KeySchema:
        - AttributeName: userId
          KeyType: HASH

Outputs:
  FunctionArn:
    Value: !GetAtt ChatFunction.Arn
```

---

**Document Version**: 1.0 | **Last Updated**: January 4, 2026 | **Next Review**: Post-hackathon debrief
