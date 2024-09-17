# Akhil Sharma's Portfolio of Projects

This repository showcases my personal projects, where I applied my skills in various domains like autonomous systems, embedded systems, full-stack development, and data structures. Below are detailed breakdowns of each project, including their technical aspects, architecture, and the specific code implementations.

---

## 1. **Dora the Explora: Autonomous Vehicle Project**
**Duration**: January – May 2024

**Project Summary**: This project involved the development of an autonomous RC car capable of navigating hallways without human intervention. The car uses LIDAR-based sensing and implements real-time mapping for navigation.

### **Technical Stack**:
- **Hardware**: Raspberry Pi, Raspberry Pi Pico, RPLIDAR A1M8
- **Software**: Python (control logic), Open3D (for 3D visualization)
- **Control System**: P (Proportional), I (Integral), and OBs (Obstacle Avoidance) terms

### **Code Breakdown**:
- **Sensors**: The RPLIDAR A1M8 sensor collects distance data in real time, processed in the Raspberry Pi.
- **Mapping**: A 3D point cloud is generated using the Open3D library. This is continuously updated as the vehicle moves.
- **Navigation**: The control system consists of PID-like parameters (P, I) for maintaining direction and an obstacle avoidance (OBs) system that dynamically adjusts speed and path based on the LIDAR data.

### **Key Files**:
- `control_system.py`: Contains the logic for vehicle movement and obstacle avoidance.
- `lidar_mapping.py`: Handles real-time data collection from RPLIDAR and visualization using Open3D.

---

## 2. **SwivelFind: Embedded Systems Final Project**
**Duration**: January – March 2024

**Project Summary**: A 360-degree swiveling rangefinder capable of detecting objects around it using an Ultrasonic Sensor. It integrates several devices, including an OLED display, a Stepper Motor, and an IR remote.

### **Technical Stack**:
- **Hardware**: Ultrasonic Sensor (UART), OLED Display (SPI), Stepper Motor (PWM)
- **Software**: Embedded C, AWS IoT (for cloud communication)

### **Code Breakdown**:
- **Sensor Communication**: UART is used for data exchange between the Ultrasonic Sensor and the microcontroller, while SPI is used to display distance readings on the OLED display.
- **Motor Control**: A stepper motor is driven using Pulse Width Modulation (PWM) for precise rotation control.
- **Remote Communication**: The IR remote control is programmed to start and stop scanning. AWS IoT is used for remote data logging.

### **Key Files**:
- `main.c`: Contains the logic for sensor readings, motor control, and communication protocols.
- `aws_iot.c`: Handles IoT communication with AWS for real-time data visualization.

---

## 3. **CEC’s Café App: Full Stack Development**
**Duration**: June 2023

**Project Summary**: This project is a full-stack web application developed for a café to manage online orders. It features a fully functional UI and integrates a backend server with a database for order management.

### **Technical Stack**:
- **Frontend**: HTML, CSS, JavaScript, Figma (for UI/UX design)
- **Backend**: Node.js, Express
- **Database**: MongoDB

### **Code Breakdown**:
- **Frontend**: The UI is designed using Figma and built using HTML and CSS. JavaScript handles form validation and async data fetching.
- **Backend**: A RESTful API built using Node.js and Express allows for CRUD operations on orders.
- **Database**: MongoDB stores user and order information. Data is retrieved and manipulated via Mongoose models.

### **Key Files**:
- `app.js`: Contains the Node.js server setup and routes.
- `order_model.js`: Mongoose schema for handling order-related database operations.
- `index.html`: Frontend code for the café's order page.

---

## 4. **Zip/Unzip Data Structures Project**
**Duration**: March – April 2022

**Project Summary**: A C/C++ project that implements a data compression algorithm using tree map data structures, reducing data storage space and improving access efficiency.

### **Technical Stack**:
- **Language**: C/C++
- **Data Structures**: Tree map (custom implementation for key-value pair storage)

### **Code Breakdown**:
- **Tree Map**: A tree map structure is used to compress and store data efficiently, improving both access and retrieval times.
- **Compression Algorithm**: The algorithm reads input data, maps each unique value to a tree node, and compresses it using a custom logic based on frequency.

### **Key Files**:
- `compression.cpp`: Handles the logic for compressing and decompressing data using tree map structures.
- `tree_map.h`: Implements the tree map data structure.

---

## 🛠 **Skills & Technologies**
- **Languages**: C, C++, Python, JavaScript, HTML/CSS
- **Frameworks & Tools**: Node.js, Express, MongoDB, AWS IoT, Open3D
- **Embedded Systems**: UART, SPI, PWM, Raspberry Pi, Pico
- **Version Control**: Git, GitHub

---

## 📝 **How to Use This Repo**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/akhil_portfolio.git
   ```
2. Navigate to any project directory and follow the README inside for project-specific instructions.

---

## 📫 **Contact**
For questions or collaborations, feel free to reach out via [LinkedIn](https://www.linkedin.com/in/akhilsharma) or [School Email](mailto:akhsharma@ucdavis.edu) or [Personal Email](mailto:theakkuking@gmail.com).
