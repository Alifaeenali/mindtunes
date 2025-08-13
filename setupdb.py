#!/usr/bin/env python3
"""
MindTune Innovations Database Setup Script
Creates database, tables, and populates initial data while avoiding duplicates
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import logging
from datetime import date, datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_setup.log'),
        logging.StreamHandler()
    ]
)

class DatabaseSetup:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'mindtunes_db')
        self.port = int(os.getenv('DB_PORT', '3306'))
        self.connection = None

    def connect_mysql(self):
        """Connect to MySQL server (without specific database)"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            logging.info("Connected to MySQL server successfully")
            return True
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            return False

    def connect_database(self):
        """Connect to specific database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            logging.info(f"Connected to database '{self.database}' successfully")
            return True
        except Error as e:
            logging.error(f"Error connecting to database: {e}")
            return False

    def create_database(self):
        """Create database if it doesn't exist"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            logging.info(f"Database '{self.database}' created/selected successfully")
            cursor.close()
            return True
        except Error as e:
            logging.error(f"Error creating database: {e}")
            return False

    def create_tables(self):
        """Create all tables with proper schema"""
        tables = {
            'navTable': """
                CREATE TABLE IF NOT EXISTS navTable (
                    nav_id INT AUTO_INCREMENT PRIMARY KEY,
                    navLogo VARCHAR(200),
                    navAnchor1 VARCHAR(200),
                    navAnchor2 VARCHAR(200),
                    navAnchor3 VARCHAR(200),
                    navAnchor4 VARCHAR(200),
                    navAnchor5 VARCHAR(200),
                    navAnchor6 VARCHAR(200)
                )
            """,
            
            'heroTable': """
                CREATE TABLE IF NOT EXISTS heroTable (
                    hero_id INT AUTO_INCREMENT PRIMARY KEY,
                    heroImg VARCHAR(200),
                    heroHead VARCHAR(500),
                    heroDesc TEXT
                )
            """,
            
            'Ourclients': """
                CREATE TABLE IF NOT EXISTS Ourclients (
                    clients_id INT AUTO_INCREMENT PRIMARY KEY,
                    clientHead VARCHAR(200),
                    clientDesc TEXT
                )
            """,
            
            'client_logos': """
                CREATE TABLE IF NOT EXISTS client_logos (
                    logo_id INT AUTO_INCREMENT PRIMARY KEY,
                    logo_url VARCHAR(255),
                    logo_order INT
                )
            """,
            
            'innovations': """
                CREATE TABLE IF NOT EXISTS innovations (
                    innovation_id INT AUTO_INCREMENT PRIMARY KEY,
                    innovationSubHead VARCHAR(200),
                    innovationHead VARCHAR(200),
                    innovationDescp VARCHAR(500),
                    innovationl1 TEXT,
                    innovationl2 TEXT,
                    innovationl3 TEXT,
                    innovationl4 TEXT,
                    innovationVideo VARCHAR(200),
                    innovationImage VARCHAR(200),
                    innovationMediaType VARCHAR(50)
                )
            """,
            
            'know': """
                CREATE TABLE IF NOT EXISTS know (
                    know_id INT AUTO_INCREMENT PRIMARY KEY,
                    knowHead VARCHAR(200),
                    knowDescp VARCHAR(500),
                    knowVideo VARCHAR(200),
                    knowImage VARCHAR(200),
                    knowMediaType VARCHAR(50),
                    knowFile VARCHAR(200)
                )
            """,
            
            'statistics': """
                CREATE TABLE IF NOT EXISTS statistics (
                    stat_id INT AUTO_INCREMENT PRIMARY KEY,
                    statHead VARCHAR(200),
                    statDescp VARCHAR(500),
                    headCard1 VARCHAR(200),
                    headCard2 VARCHAR(200),
                    headCard3 VARCHAR(200),
                    DescCard1 VARCHAR(200),
                    DescCard2 VARCHAR(200),
                    DescCard3 VARCHAR(200),
                    ImgCard1 VARCHAR(200),
                    ImgCard2 VARCHAR(200),
                    ImgCard3 VARCHAR(200)
                )
            """,
            
            'footer': """
                CREATE TABLE IF NOT EXISTS footer (
                    ftr_id INT AUTO_INCREMENT PRIMARY KEY,
                    ftr_link1 VARCHAR(200),
                    ftr_link2 VARCHAR(200),
                    ftr_link3 VARCHAR(200),
                    ftr_link4 VARCHAR(200)
                )
            """,
            
            'aboutUs': """
                CREATE TABLE IF NOT EXISTS aboutUs (
                    about_id INT AUTO_INCREMENT PRIMARY KEY,
                    about_head VARCHAR(200),
                    about_desc TEXT,
                    about_title VARCHAR(500),
                    about_subtitle VARCHAR(500),
                    about_secondary_desc TEXT,
                    aboutHeroImage VARCHAR(200),
                    achievement_title VARCHAR(200),
                    achievement_subtitle TEXT,
                    mission_text TEXT,
                    belief1 VARCHAR(500),
                    belief2 VARCHAR(500),
                    belief3 VARCHAR(500),
                    belief4 VARCHAR(500)
                )
            """,
            
            'founders': """
                CREATE TABLE IF NOT EXISTS founders (
                    founder_id INT AUTO_INCREMENT PRIMARY KEY,
                    founder_name VARCHAR(200),
                    founder_role VARCHAR(200),
                    founder_image VARCHAR(200),
                    founder_description TEXT,
                    founder_order INT
                )
            """,
            
            'who_we_work_with': """
                CREATE TABLE IF NOT EXISTS who_we_work_with (
                    work_id INT AUTO_INCREMENT PRIMARY KEY,
                    work_icon VARCHAR(20),
                    work_title VARCHAR(200),
                    work_description TEXT,
                    work_order INT
                )
            """,
            
            'servicesTable': """
                CREATE TABLE IF NOT EXISTS servicesTable (
                    service_id INT AUTO_INCREMENT PRIMARY KEY,
                    service_head VARCHAR(200),
                    service_desc TEXT,
                    service_icon VARCHAR(255) DEFAULT 'fas fa-cogs'
                )
            """,
            
            'blog_posts': """
                CREATE TABLE IF NOT EXISTS blog_posts (
                    blog_id INT AUTO_INCREMENT PRIMARY KEY,
                    blog_title VARCHAR(255) NOT NULL,
                    blog_subtitle VARCHAR(255),
                    blog_author VARCHAR(100) NOT NULL,
                    blog_date DATE NOT NULL,
                    blog_image VARCHAR(255),
                    blog_excerpt TEXT,
                    blog_content LONGTEXT NOT NULL,
                    blog_status ENUM('draft', 'published') DEFAULT 'published',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """,
            
            'job_postings': """
                CREATE TABLE IF NOT EXISTS job_postings (
                    job_id INT AUTO_INCREMENT PRIMARY KEY,
                    job_title VARCHAR(255) NOT NULL,
                    job_type ENUM('full-time', 'part-time', 'internship', 'contract') NOT NULL,
                    department VARCHAR(100) NOT NULL,
                    location VARCHAR(100) NOT NULL,
                    salary_range VARCHAR(100),
                    job_description LONGTEXT NOT NULL,
                    requirements LONGTEXT NOT NULL,
                    responsibilities LONGTEXT NOT NULL,
                    benefits TEXT,
                    application_deadline DATE,
                    job_status ENUM('active', 'closed', 'draft') DEFAULT 'active',
                    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """,
            
            'job_applications': """
                CREATE TABLE IF NOT EXISTS job_applications (
                    application_id INT AUTO_INCREMENT PRIMARY KEY,
                    job_id INT NOT NULL,
                    applicant_name VARCHAR(255) NOT NULL,
                    applicant_email VARCHAR(255) NOT NULL,
                    applicant_phone VARCHAR(20),
                    cover_letter TEXT,
                    cv_filename VARCHAR(255) NOT NULL,
                    cv_path VARCHAR(500) NOT NULL,
                    linkedin_profile VARCHAR(255),
                    portfolio_website VARCHAR(255),
                    expected_salary VARCHAR(100),
                    availability_date DATE,
                    application_status ENUM('pending', 'reviewed', 'shortlisted', 'interviewed', 'hired', 'rejected') DEFAULT 'pending',
                    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (job_id) REFERENCES job_postings(job_id) ON DELETE CASCADE
                )
            """,
            
            'contact_submissions': """
                CREATE TABLE IF NOT EXISTS contact_submissions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    subject VARCHAR(255),
                    message TEXT,
                    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            'team_members': """
                CREATE TABLE IF NOT EXISTS team_members (
                    team_id INT AUTO_INCREMENT PRIMARY KEY,
                    member_name VARCHAR(255) NOT NULL,
                    member_position VARCHAR(255) NOT NULL,
                    member_description TEXT NOT NULL,
                    member_image VARCHAR(500) NOT NULL,
                    team_order INT DEFAULT 1,
                    member_status ENUM('active', 'inactive') DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """
        }

        try:
            cursor = self.connection.cursor()
            for table_name, create_sql in tables.items():
                cursor.execute(create_sql)
                logging.info(f"Table '{table_name}' created successfully")
            
            # Create indexes
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_submission_date ON contact_submissions (submission_date)",
                "CREATE INDEX IF NOT EXISTS idx_blog_status ON blog_posts (blog_status)",
                "CREATE INDEX IF NOT EXISTS idx_job_status ON job_postings (job_status)",
                "CREATE INDEX IF NOT EXISTS idx_application_status ON job_applications (application_status)"
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
            
            cursor.close()
            logging.info("All tables and indexes created successfully")
            return True
        except Error as e:
            logging.error(f"Error creating tables: {e}")
            return False

    def check_duplicate(self, table, condition_field, condition_value):
        """Check if record already exists"""
        try:
            cursor = self.connection.cursor()
            query = f"SELECT COUNT(*) FROM {table} WHERE {condition_field} = %s"
            cursor.execute(query, (condition_value,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except Error as e:
            logging.error(f"Error checking duplicate: {e}")
            return False

    def insert_data(self):
        """Insert initial data into tables"""
        try:
            cursor = self.connection.cursor()

            # Navigation data
            if not self.check_duplicate('navTable', 'navAnchor1', 'Home'):
                nav_data = {
                    'navLogo': '/static/uploads/WhatsApp_Image_2025-03-25_at_14.06.11_4d5129c4-removebg-preview_1_1755060269.png',
                    'navAnchor1': 'Home',
                    'navAnchor2': 'About',
                    'navAnchor3': 'Services',
                    'navAnchor4': 'News',
                    'navAnchor5': 'Contact Us',
                    'navAnchor6': 'Careers'
                }
                cursor.execute("""
                    INSERT INTO navTable (navLogo, navAnchor1, navAnchor2, navAnchor3, navAnchor4, navAnchor5, navAnchor6)
                    VALUES (%(navLogo)s, %(navAnchor1)s, %(navAnchor2)s, %(navAnchor3)s, %(navAnchor4)s, %(navAnchor5)s, %(navAnchor6)s)
                """, nav_data)
                logging.info("Navigation data inserted")

            # Hero data
            if not self.check_duplicate('heroTable', 'heroHead', 'We Engineer Next-Gen Wearables, Smart IoT Products & Full-Stack Tech Solutions updated'):
                hero_data = {
                    'heroImg': '/static/uploads/hero_1755007641.png',
                    'heroHead': 'We Engineer Next-Gen Wearables, Smart IoT Products & Full-Stack Tech Solutions updated',
                    'heroDesc': 'At MindTune Innovations, we help you bring bold product ideas to life. From connected devices to powerful software, our team handles every step including hardware, firmware, mobile apps, and mechanical design all under one roof. Whether you\'re a startup, research team, or enterprise, we deliver complete and ready-to-deploy solutions that are reliable, scalable, and user-friendly. updated'
                }
                cursor.execute("""
                    INSERT INTO heroTable (heroImg, heroHead, heroDesc)
                    VALUES (%(heroImg)s, %(heroHead)s, %(heroDesc)s)
                """, hero_data)
                logging.info("Hero data inserted")

            # Client data
            if not self.check_duplicate('Ourclients', 'clientHead', 'Trusted by Leading Innovators'):
                client_data = {
                    'clientHead': 'Trusted by Leading Innovators',
                    'clientDesc': 'Our clientele includes a diverse range of companies, from tech startups to healthcare providers, all seeking to leverage the power of sound for human flourishing.'
                }
                cursor.execute("""
                    INSERT INTO Ourclients (clientHead, clientDesc)
                    VALUES (%(clientHead)s, %(clientDesc)s)
                """, client_data)
                logging.info("Client data inserted")

            # Client logos
            client_logos = [
                ('/static/uploads/client1_1754991075.png', 1),
                ('/static/uploads/client2_1754991075.png', 2),
                ('/static/uploads/mindtunes_1_1755010632.png', 3)
            ]
            for logo_url, logo_order in client_logos:
                if not self.check_duplicate('client_logos', 'logo_url', logo_url):
                    cursor.execute("INSERT INTO client_logos (logo_url, logo_order) VALUES (%s, %s)", (logo_url, logo_order))
            logging.info("Client logos inserted")

            # Innovations data
            if not self.check_duplicate('innovations', 'innovationHead', 'Neuro-Acoustic Innovations'):
                innovation_data = {
                    'innovationSubHead': 'Pioneering the Future',
                    'innovationHead': 'Neuro-Acoustic Innovations',
                    'innovationDescp': 'Discover how our proprietary algorithms and sound frequencies are revolutionizing mental performance and relaxation. We integrate the latest neuroscience with artistic sound design.',
                    'innovationl1': 'Personalized Brainwave Entrainment for focus and calm.',
                    'innovationl2': 'Adaptive Soundscapes that respond to your real-time biometric data.',
                    'innovationl3': 'Gamified Cognitive Training modules for enhanced learning.',
                    'innovationl4': 'Proprietary AI-driven sound generation for unique experiences.',
                    'innovationVideo': 'static/assets/videos/a_new_course.webm',
                    'innovationImage': 'static/assets/images/hero.png',
                    'innovationMediaType': 'video'
                }
                cursor.execute("""
                    INSERT INTO innovations (innovationSubHead, innovationHead, innovationDescp, innovationl1, 
                    innovationl2, innovationl3, innovationl4, innovationVideo, innovationImage, innovationMediaType)
                    VALUES (%(innovationSubHead)s, %(innovationHead)s, %(innovationDescp)s, %(innovationl1)s, 
                    %(innovationl2)s, %(innovationl3)s, %(innovationl4)s, %(innovationVideo)s, %(innovationImage)s, %(innovationMediaType)s)
                """, innovation_data)
                logging.info("Innovation data inserted")

            # About Us data
            if not self.check_duplicate('aboutUs', 'about_head', 'About MindTune Innovations'):
                about_data = {
                    'about_head': 'About MindTune Innovations',
                    'about_desc': 'Building intelligent products that connect hardware, software, and people',
                    'about_title': 'About Us',
                    'about_subtitle': 'MindTune Innovations is a technology company based in Pakistan, focused on building intelligent products that connect hardware, software, and people. We bring together expertise in IoT, embedded systems, wearable tech, PCB design, and mobile app development — all within one team.',
                    'about_secondary_desc': 'MindTune Innovations is a technology company based in Pakistan, focused on building intelligent products that connect hardware, software, and people. We bring together expertise in IoT, embedded systems, wearable tech, PCB design, and mobile app development — all within one team.',
                    'aboutHeroImage': '/static/uploads/mindtuneteam_1754838288_1754898947.png',
                    'achievement_title': 'Innovation & Excellence',
                    'achievement_subtitle': 'Leading the way in wearable technology and IoT solutions with cutting-edge research and development.',
                    'mission_text': 'Our mission is to bridge the gap between advanced technology and everyday life by creating intelligent, user-friendly products that enhance human capabilities and well-being.',
                    'belief1': 'Innovation drives progress',
                    'belief2': 'Quality over quantity',
                    'belief3': 'User-centered design',
                    'belief4': 'Collaborative excellence'
                }
                cursor.execute("""
                    INSERT INTO aboutUs (about_head, about_desc, about_title, about_subtitle, about_secondary_desc, 
                    aboutHeroImage, achievement_title, achievement_subtitle, mission_text, belief1, belief2, belief3, belief4)
                    VALUES (%(about_head)s, %(about_desc)s, %(about_title)s, %(about_subtitle)s, %(about_secondary_desc)s,
                    %(aboutHeroImage)s, %(achievement_title)s, %(achievement_subtitle)s, %(mission_text)s, 
                    %(belief1)s, %(belief2)s, %(belief3)s, %(belief4)s)
                """, about_data)
                logging.info("About Us data inserted")

            # Founders data
            founders_data = [
                {
                    'founder_name': 'Abdul Basit',
                    'founder_role': 'CEO & DIRECTOR',
                    'founder_image': 'static/assets/images/abbasit.png',
                    'founder_description': 'Abdul Basit is an Electrical Engineer and technology innovator with a proven track record in developing high-performance IoT and smart electronic solutions. At MindTune Innovations, he leads the company\'s product development strategy, combining technical depth in hardware and embedded systems with a clear vision for scalable, market-ready solutions. His focus is on building products that deliver measurable value and position MindTune as a leader in EEG and IoT-driven technologies.',
                    'founder_order': 1
                },
                {
                    'founder_name': 'Ryan Ahmed',
                    'founder_role': 'COO & DIRECTOR',
                    'founder_image': 'static/assets/images/rayanAhmed.png',
                    'founder_description': 'Ryan Ahmed is the Co-Founder of Niura and a strategic leader in wearable neuroscience technologies. With a background in launching and scaling consumer tech ventures, Ryan has positioned Niura as a pioneer in EEG-powered earbuds designed for mental performance tracking. His expertise in bridging neuroscience with consumer technology allows Niura and MindTune to capture emerging market opportunities and drive significant growth potential in the wearable tech space.',
                    'founder_order': 2
                }
            ]
            
            for founder in founders_data:
                if not self.check_duplicate('founders', 'founder_name', founder['founder_name']):
                    cursor.execute("""
                        INSERT INTO founders (founder_name, founder_role, founder_image, founder_description, founder_order)
                        VALUES (%(founder_name)s, %(founder_role)s, %(founder_image)s, %(founder_description)s, %(founder_order)s)
                    """, founder)
            logging.info("Founders data inserted")

            # Services data
            services_data = [
                {
                    'service_head': 'IoT & Embedded Systems Development',
                    'service_desc': 'We design and build smart IoT solutions powered by efficient embedded systems, enabling seamless device connectivity, data collection, and automation for consumer and industrial applications. Our engineers specialize in microcontrollers, sensors, and wireless protocols for optimized performance.',
                    'service_icon': 'fa-solid fa-laptop'
                },
                {
                    'service_head': 'EEG Wearables & Biosensor Solutions',
                    'service_desc': 'MindTune pioneers EEG-powered wearables and biosensor integrations, enabling real-time tracking of mental and physical states. From earbuds to headsets, we turn neuroscience into user-friendly products for health, productivity, and research markets.',
                    'service_icon': 'fa-solid fa-microchip'
                },
                {
                    'service_head': 'PCB Design & Hardware Prototyping',
                    'service_desc': 'Our hardware team delivers PCB designs and rapid prototypes that meet high standards of performance, efficiency, and reliability. We handle every stage — from schematics to assembled boards.',
                    'service_icon': 'fa-solid fa-wrench'
                },
                {
                    'service_head': 'Firmware & Machine Learning Integration',
                    'service_desc': 'We create efficient firmware optimized for real-time data and integrate machine learning algorithms to deliver intelligent, adaptive devices. Our systems enhance performance while enabling edge-level AI features.',
                    'service_icon': 'fa-solid fa-robot'
                },
                {
                    'service_head': 'Mobile App & Cloud Development',
                    'service_desc': 'We build scalable mobile apps and cloud platforms to connect devices, users, and data seamlessly. From Bluetooth integration to cloud dashboards, we bring IoT ecosystems to life.',
                    'service_icon': 'fas fa-mobile-alt'
                },
                {
                    'service_head': 'Product Design & Mechanical CAD',
                    'service_desc': 'Our mechanical engineers create functional and aesthetically refined designs using advanced CAD tools. We design housings, enclosures, and product structures that are production-ready.',
                    'service_icon': 'fa-solid fa-hard-drive'
                }
            ]
            
            for service in services_data:
                if not self.check_duplicate('servicesTable', 'service_head', service['service_head']):
                    cursor.execute("""
                        INSERT INTO servicesTable (service_head, service_desc, service_icon)
                        VALUES (%(service_head)s, %(service_desc)s, %(service_icon)s)
                    """, service)
            logging.info("Services data inserted")

            # Footer data
            if not self.check_duplicate('footer', 'ftr_link1', 'Privacy Policy'):
                footer_data = {
                    'ftr_link1': 'Privacy Policy',
                    'ftr_link2': 'Terms of Service',
                    'ftr_link3': 'Info@mindtuneinnovation.tech',
                    'ftr_link4': 'https://www.linkedin.com/company/mindtune-innovations'
                }
                cursor.execute("""
                    INSERT INTO footer (ftr_link1, ftr_link2, ftr_link3, ftr_link4)
                    VALUES (%(ftr_link1)s, %(ftr_link2)s, %(ftr_link3)s, %(ftr_link4)s)
                """, footer_data)
                logging.info("Footer data inserted")

            # Statistics data
            if not self.check_duplicate('statistics', 'statHead', 'Impact and Achievements'):
                stats_data = {
                    'statHead': 'Impact and Achievements',
                    'statDescp': 'See the measurable difference MindTunes is making in people\'s lives and in various industries. Our data speaks volumes.',
                    'headCard1': '90% Improvement',
                    'headCard2': '20K+ Users',
                    'headCard3': '15+ Patents',
                    'DescCard1': 'Users report significant improvement in focus and sleep quality.',
                    'DescCard2': 'Global community benefiting from MindTunes daily.',
                    'DescCard3': 'Cutting-edge technology protected by intellectual property.',
                    'ImgCard1': '/static/uploads/stats1_1754841602_1754898914.png',
                    'ImgCard2': '/static/uploads/stats2_1754841602_1754898914.png',
                    'ImgCard3': '/static/uploads/stats3_1754841602_1754898914.png'
                }
                cursor.execute("""
                    INSERT INTO statistics (statHead, statDescp, headCard1, headCard2, headCard3, 
                    DescCard1, DescCard2, DescCard3, ImgCard1, ImgCard2, ImgCard3)
                    VALUES (%(statHead)s, %(statDescp)s, %(headCard1)s, %(headCard2)s, %(headCard3)s,
                    %(DescCard1)s, %(DescCard2)s, %(DescCard3)s, %(ImgCard1)s, %(ImgCard2)s, %(ImgCard3)s)
                """, stats_data)
                logging.info("Statistics data inserted")

            # Who we work with data
            work_with_data = [
                ('🏥', 'Health-Tech Startups', 'Building wearable products and health monitoring solutions', 1),
                ('⚙️', 'Engineering Teams', 'Embedded systems and PCB development support', 2),
                ('🔬', 'Research Labs', 'Developing biomedical and IoT research tools', 3),
                ('🏢', 'Enterprise Companies', 'Custom hardware with mobile and cloud integration', 4)
            ]
            
            for icon, title, desc, order in work_with_data:
                if not self.check_duplicate('who_we_work_with', 'work_title', title):
                    cursor.execute("""
                        INSERT INTO who_we_work_with (work_icon, work_title, work_description, work_order)
                        VALUES (%s, %s, %s, %s)
                    """, (icon, title, desc, order))
            logging.info("Who we work with data inserted")

            # Team members data
            team_data = [
                {
                    'member_name': 'John Smith',
                    'member_position': 'Lead Developer',
                    'member_description': 'Experienced full-stack developer with expertise in modern web technologies and system architecture.',
                    'member_image': '/static/uploads/usericon_1754982255.png',
                    'team_order': 1
                },
                {
                    'member_name': 'Sarah Johnson',
                    'member_position': 'UI/UX Designer',
                    'member_description': 'Creative designer focused on user experience and interface design with a passion for creating intuitive solutions.',
                    'member_image': '/static/uploads/usericon_1754982255.png',
                    'team_order': 2
                },
                {
                    'member_name': 'Mike Chen',
                    'member_position': 'Project Manager',
                    'member_description': 'Skilled project manager ensuring smooth delivery of projects while maintaining quality and client satisfaction.',
                    'member_image': '/static/uploads/usericon_1754982255.png',
                    'team_order': 3
                }
            ]
            
            for member in team_data:
                if not self.check_duplicate('team_members', 'member_name', member['member_name']):
                    cursor.execute("""
                        INSERT INTO team_members (member_name, member_position, member_description, member_image, team_order)
                        VALUES (%(member_name)s, %(member_position)s, %(member_description)s, %(member_image)s, %(team_order)s)
                    """, member)
            logging.info("Team members data inserted")

            self.connection.commit()
            cursor.close()
            logging.info("All initial data inserted successfully")
            return True
            
        except Error as e:
            logging.error(f"Error inserting data: {e}")
            self.connection.rollback()
            return False

    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Database connection closed")

    def setup_complete_database(self):
        """Complete database setup process"""
        try:
            # Connect to MySQL server
            if not self.connect_mysql():
                return False

            # Create database
            if not self.create_database():
                return False

            # Close connection and reconnect to specific database
            self.close_connection()
            if not self.connect_database():
                return False

            # Create tables
            if not self.create_tables():
                return False

            # Insert initial data
            if not self.insert_data():
                return False

            logging.info("Database setup completed successfully!")
            return True

        except Exception as e:
            logging.error(f"Error during database setup: {e}")
            return False
        finally:
            self.close_connection()


def main():
    """Main function to run the database setup"""
    print("Starting MindTune Innovations Database Setup...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Warning: .env file not found. Using default database connection settings.")
        print("Create a .env file with the following variables:")
        print("DB_HOST=localhost")
        print("DB_USER=root")
        print("DB_PASSWORD=your_password")
        print("DB_NAME=mindtunes_db")
        print("DB_PORT=3306")
        print()

    db_setup = DatabaseSetup()
    
    if db_setup.setup_complete_database():
        print("✅ Database setup completed successfully!")
        print(f"✅ Database '{db_setup.database}' is ready to use")
        print("✅ All tables created and populated with initial data")
    else:
        print("❌ Database setup failed. Check the logs for details.")
        return False

    return True


if __name__ == "__main__":
    main()