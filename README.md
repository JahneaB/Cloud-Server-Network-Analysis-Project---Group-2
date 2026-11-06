# ☁️ 🛜 Cloud-Server-Network-Analysis-Project - Group-2

Members:
Juliana Ariza
Justine Bailey
Jahnea Bush
Blake Thomas

## Project Objective:
The primary objective is to design, implement, and evaluate a distributed file- sharing system in the cloud employing a server-client architecture. The system will facilitate efficient and secure file transfer between multiple clients connected to a central server.

## Member Roles:

## 🛜 Juliana:

Network Analysis Application Design
(Shared with Blake)

- Implement a module that collects statistics from either server and/or client applications
- Module should start with the server application.
- Network statistics including upload/download data rates, file transfer times and a third metric of your choice stored (ie dictionary or dataframe) to be reviewed offline. (This data will be used for the report)


## 🖥️ Justine:

Server Application Design

- Create a multithreaded server to handle multiple client
connections simultaneously.
- Implement data structures (e.g., file system, client connection
pool) to efficiently manage files and client information.
- Utilize logical file naming conventions that identifies the file
type (ie text vs video) while avoiding duplicate file names. (ie
TS001 for Text-Server file)
- Implement file transfer logic using appropriate network
protocols.
- Handle authentication and authorization requests.
- Server-Side application must be deployed to Google Cloud
Platform -Compute Engine.

## 👨‍💻 Jahnea:
Client Side Application Design
 
 - Implement a user interface for clients to interact with the file
   sharing system.
- Implement network communication logic to connect to the
  server and send/receive file requests.
- Handle file uploads, downloads, and directory operations.
- Provide feedback to the user regarding the status of file
  transfers and operations.
- Clide-side applications may be used from students’ personal computers or deployed to a separate Google Cloud Platform Compute Engine instance.


## 🛜 Blake:

Network Analysis Application Design
(Shared with Juliana)

- Implement a module that collects statistics from either server and/or client applications
- Module should start with the server application.
- Network statistics including upload/download data rates, file transfer times and a third metric of your choice stored (ie dictionary or dataframe) to be reviewed offline. (This data will be used for the report)


