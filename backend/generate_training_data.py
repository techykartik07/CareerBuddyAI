"""
generate_training_data.py
Generates a synthetic resume dataset for the job role classifier.
Covers 25 job categories with realistic keyword patterns.
Run once to create data/Resume.csv, then run train_classifier.py.
"""

import os, random, csv

random.seed(42)

# ── Category definitions ───────────────────────────────────────────────────
CATEGORIES = {
    "Data Science": [
        "machine learning deep learning python pandas numpy scikit-learn tensorflow keras pytorch "
        "data analysis statistics regression classification clustering neural networks nlp "
        "jupyter notebook matplotlib seaborn data wrangling feature engineering model evaluation "
        "random forest gradient boosting xgboost lightgbm cross-validation hyperparameter tuning "
        "data pipeline etl big data spark hadoop sql database statistical analysis hypothesis testing "
        "a/b testing data visualization tableau power bi r programming statistical modeling "
        "natural language processing text mining computer vision image recognition transformers bert "
        "time series forecasting anomaly detection recommendation system collaborative filtering",
    ],
    "Software Engineering": [
        "java python c++ software development object-oriented programming design patterns "
        "algorithms data structures system design microservices rest api spring boot hibernate "
        "unit testing integration testing ci/cd jenkins git github agile scrum jira "
        "software architecture distributed systems multithreading concurrency code review "
        "software development lifecycle sdlc version control documentation debugging profiling "
        "solid principles clean code refactoring performance optimization low latency "
        "kafka message queues event-driven architecture grpc protocol buffers",
    ],
    "Web Development": [
        "html css javascript typescript react angular vue.js node.js express.js "
        "frontend backend full stack web application responsive design bootstrap tailwind "
        "rest api graphql webpack babel npm yarn redux react hooks state management "
        "next.js gatsby single page application spa progressive web app pwa "
        "browser compatibility cross-platform web performance lighthouse seo "
        "sass scss styled-components testing jest cypress web sockets real-time "
        "authentication authorization oauth jwt session management",
    ],
    "Android Development": [
        "android kotlin java android studio xml firebase google play sdk "
        "mvvm architecture viewmodel livedata databinding room database retrofit "
        "material design fragments activities intents broadcast receivers services "
        "background tasks workmanager coroutines flow jetpack compose "
        "push notifications firebase cloud messaging google maps api "
        "unit testing espresso mockito gradle build system apk aab release "
        "android permissions bluetooth gps camera media playback",
    ],
    "iOS Development": [
        "swift objective-c xcode ios iphone ipad app store apple "
        "uikit swiftui auto layout core data alamofire cocoapods spm "
        "mvvm mvc viper combine reactive programming "
        "push notifications apns core location mapkit "
        "arkit metal core animation animations transitions "
        "in-app purchase subscription receipt validation "
        "unit testing xctest simulator instruments performance profiling",
    ],
    "DevOps": [
        "docker kubernetes jenkins ci/cd pipeline infrastructure as code terraform ansible "
        "aws azure gcp cloud computing linux bash shell scripting "
        "monitoring observability prometheus grafana elk stack log aggregation "
        "site reliability sre availability reliability scalability "
        "nginx load balancing service mesh istio helm charts "
        "git branching strategy deployment strategies blue green canary "
        "security hardening compliance vulnerability scanning",
    ],
    "Cloud Computing": [
        "aws amazon web services ec2 s3 rds lambda cloudformation vpc "
        "azure active directory blob storage cosmos db app service "
        "gcp google cloud bigquery cloud run cloud functions "
        "cloud architecture multi-cloud hybrid cloud cost optimisation "
        "serverless functions containers microservices kubernetes "
        "cloud security iam roles policies compliance certifications "
        "cloud migration lift shift devops cloud native sla slo",
    ],
    "Cybersecurity": [
        "network security penetration testing ethical hacking vulnerability assessment "
        "firewall ids ips siem log analysis threat intelligence incident response "
        "cryptography ssl tls pki encryption decryption "
        "owasp top 10 web application security sql injection xss csrf "
        "kali linux nmap metasploit burp suite wireshark "
        "iso 27001 nist gdpr compliance security audit "
        "security operations soc analyst malware analysis reverse engineering "
        "zero trust architecture endpoint security antivirus edr",
    ],
    "Database Administration": [
        "mysql postgresql oracle sql server mongodb redis elasticsearch "
        "database design normalization indexing query optimization "
        "backup recovery disaster recovery high availability replication "
        "stored procedures triggers views transactions acid properties "
        "database migration schema design erd entity relationship "
        "nosql document store key-value graph database "
        "performance tuning explain plans slow query analysis "
        "data warehousing etl data lake olap oltp",
    ],
    "Machine Learning Engineer": [
        "mlops model deployment model serving tensorflow serving torchserve "
        "feature store feature engineering pipeline automation "
        "docker kubernetes model monitoring drift detection "
        "python scikit-learn tensorflow pytorch xgboost "
        "a/b testing model evaluation metrics precision recall f1 auc roc "
        "data versioning dvc mlflow experiment tracking "
        "distributed training gpu cuda parallel computing "
        "nlp transformers bert gpt fine-tuning embeddings",
    ],
    "Artificial Intelligence": [
        "artificial intelligence neural networks deep learning computer vision "
        "natural language processing generative ai llm large language models "
        "reinforcement learning q-learning dqn policy gradient "
        "object detection yolo image segmentation face recognition "
        "speech recognition text-to-speech sentiment analysis "
        "gpt chatgpt openai prompt engineering rag retrieval augmented generation "
        "diffusion models stable diffusion image generation "
        "ai ethics responsible ai bias fairness explainability",
    ],
    "Business Analyst": [
        "business analysis requirements gathering stakeholder management "
        "use cases user stories epics backlog grooming "
        "uml flowcharts process mapping bpmn "
        "excel pivot tables vlookup data analysis reporting "
        "power bi tableau business intelligence dashboard kpi metrics "
        "sql database querying data extraction "
        "agile scrum product owner sprint planning "
        "gap analysis as-is to-be process improvement "
        "cost benefit analysis roi business case",
    ],
    "Project Manager": [
        "project management pmp prince2 agile waterfall "
        "project planning scheduling gantt chart microsoft project "
        "risk management risk register mitigation contingency "
        "stakeholder management communication leadership "
        "budget management cost control resource allocation "
        "scope management change management "
        "jira confluence trello project tracking "
        "team leadership cross-functional coordination "
        "vendor management contracts procurement",
    ],
    "Digital Marketing": [
        "seo sem google analytics google ads facebook ads "
        "content marketing email marketing social media marketing "
        "conversion rate optimization cro landing pages a/b testing "
        "hubspot salesforce crm marketing automation "
        "ppc pay-per-click display advertising remarketing "
        "keyword research backlink building on-page off-page seo "
        "instagram linkedin twitter youtube influencer marketing "
        "brand awareness lead generation funnel campaign management",
    ],
    "HR": [
        "human resources recruitment talent acquisition onboarding "
        "performance management employee engagement retention "
        "hris payroll compensation benefits administration "
        "training development learning management system lms "
        "labor law compliance ada eeoc fmla "
        "succession planning workforce planning headcount "
        "diversity inclusion equity belonging "
        "employee relations grievance handling exit interview "
        "job description job evaluation hay method grading",
    ],
    "Finance": [
        "financial analysis financial modeling excel valuation "
        "balance sheet income statement cash flow dcf analysis "
        "investment banking mergers acquisitions private equity "
        "portfolio management risk management hedge fund "
        "accounting ifrs gaap auditing tax compliance "
        "bloomberg reuters financial data equity research "
        "budgeting forecasting variance analysis kpi "
        "cfa cpa chartered accountant financial reporting",
    ],
    "Graphic Design": [
        "adobe photoshop illustrator indesign after effects premiere "
        "ui design ux design user experience wireframing prototyping "
        "figma sketch invision xd adobe xd "
        "branding logo design typography color theory "
        "motion graphics animation video editing "
        "print design packaging design social media graphics "
        "responsive design grid systems visual hierarchy "
        "design thinking user research usability testing",
    ],
    "Sales": [
        "sales business development account management b2b b2c "
        "lead generation prospecting cold calling outbound inbound "
        "crm salesforce hubspot pipeline management "
        "negotiation closing deals contract management "
        "revenue target quota attainment commission "
        "customer relationship management upselling cross-selling "
        "sales strategy market penetration competitive analysis "
        "product demonstration presentation skills pitch deck",
    ],
    "Network Engineer": [
        "cisco networking routers switches vlans spanning tree "
        "tcp/ip dns dhcp bgp ospf eigrp routing protocols "
        "firewall vpn ipsec ssl network security "
        "network monitoring snmp netflow wireshark "
        "lan wan sd-wan mpls fiber optic "
        "ccna ccnp network certification "
        "network design topology subnetting ip addressing "
        "troubleshooting packet analysis latency bandwidth",
    ],
    "Embedded Systems": [
        "c c++ embedded systems microcontroller microprocessor "
        "arduino raspberry pi stm32 atmel pic "
        "rtos real time operating system freertos "
        "uart spi i2c communication protocols "
        "pcb design schematic altium eagle kicad "
        "firmware development bootloader interrupt handling "
        "signal processing adc dac gpio pwm timers "
        "iot internet of things mqtt coap wifi bluetooth zigbee "
        "low power design battery optimization sleep modes",
    ],
    "Testing / QA": [
        "software testing quality assurance manual testing automated testing "
        "selenium cypress playwright test automation framework "
        "jmeter performance testing load testing stress testing "
        "api testing postman rest assured test cases test plan "
        "bug reporting defect lifecycle jira test management "
        "regression testing smoke testing sanity testing "
        "agile testing bdd tdd gherkin cucumber "
        "mobile testing appium android ios "
        "database testing sql query validation",
    ],
    "Blockchain": [
        "blockchain solidity ethereum smart contracts web3.js ethers.js "
        "truffle hardhat remix defi decentralized finance "
        "nft non-fungible token erc-20 erc-721 "
        "consensus algorithms proof of work proof of stake "
        "cryptography hash functions merkle tree "
        "hyperledger fabric enterprise blockchain "
        "dao governance tokenomics white paper "
        "dapp decentralized application frontend react integration "
        "audit security vulnerability reentrancy attack",
    ],
    "Data Analyst": [
        "sql excel power bi tableau data visualization "
        "data cleaning data wrangling pivot table vlookup "
        "python pandas numpy matplotlib seaborn "
        "statistical analysis descriptive statistics "
        "dashboard reporting kpi metrics business intelligence "
        "google analytics google sheets data studio "
        "etl data pipeline database querying "
        "a/b testing hypothesis testing survey analysis "
        "presentation insights stakeholder communication",
    ],
    "Mechanical Engineer": [
        "autocad solidworks catia ansys finite element analysis "
        "mechanical design manufacturing cad cam "
        "thermodynamics fluid mechanics heat transfer "
        "materials science metallurgy polymer composite "
        "cnc machining lathes milling turning "
        "product design prototyping tolerance analysis "
        "six sigma lean manufacturing quality control "
        "gd&t welding casting forging "
        "project management bom bill of materials",
    ],
    "Civil Engineering": [
        "autocad staad pro etabs revit bim "
        "structural analysis concrete steel reinforced "
        "foundation design geotechnical survey "
        "construction management project planning site supervision "
        "quantity estimation bill of quantities tender "
        "roads highways bridges drainage sewage "
        "environmental compliance permit regulatory "
        "surveying leveling total station gps "
        "quality control testing concrete compressive strength",
    ],
}

def make_resume(category: str, keywords_blob: str, n_words: int = 120) -> str:
    """Shuffle keywords and pad with filler sentences to mimic real resume text."""
    words = keywords_blob.split()
    random.shuffle(words)
    selected = words[:n_words]
    text = " ".join(selected)

    fillers = [
        f"Experienced {category} professional with strong background in relevant technologies.",
        "Proven track record of delivering high-quality results on time.",
        "Strong communication and collaboration skills in cross-functional teams.",
        "Passionate about solving complex problems and continuous learning.",
        f"Looking for a challenging {category} role in a growth-oriented organization.",
        "Bachelor's degree in Computer Science / Engineering or equivalent.",
        "3+ years of hands-on industry experience.",
    ]
    random.shuffle(fillers)
    combined = text + " " + " ".join(fillers[:3])
    return combined


def generate_dataset(samples_per_category: int = 100) -> list[dict]:
    rows = []
    for category, blobs in CATEGORIES.items():
        blob = " ".join(blobs)
        for _ in range(samples_per_category):
            n = random.randint(80, 140)
            resume_text = make_resume(category, blob, n)
            rows.append({"Category": category, "Resume": resume_text})
    random.shuffle(rows)
    return rows


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    print("Generating synthetic resume training data...")
    rows = generate_dataset(samples_per_category=120)
    out_path = "data/Resume.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Category", "Resume"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} samples across {len(CATEGORIES)} categories → {out_path}")
