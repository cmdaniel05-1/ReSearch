# Project Design Document
## ReSearch
--------
Prepared by:
* `Ian Wood`,`WPI>`
* `Sarah Meyer`,`WPI`
* `April Zingher`,`WPI`
* `Connor Daniel`,`WPI`
---
**Course** : CS 3733 - Software Engineering
**Instructor**: Sakire Arslan Ay
---
## Table of Contents
- [Project Design Document](#project-design-document)
  - [ReSearch](#research)
  - [**Instructor**: Sakire Arslan Ay](#instructor-sakire-arslan-ay)
  - [Table of Contents](#table-of-contents)
    - [Document Revision History](#document-revision-history)
- [1. Introduction](#1-introduction)
- [2. Software Design](#2-software-design)
  - [2.1 Database Model](#21-database-model)
  - [2.2 Modules and Interfaces](#22-modules-and-interfaces)
    - [2.2.1 Overview](#221-overview)
    - [2.2.2 Interfaces](#222-interfaces)
      - [2.2.2.1 \<Auth\> Routes](#2221-auth-routes)
      - [2.2.2.2 \<Main\> Routes](#2222-main-routes)
    - [2.3 User Interface Design](#23-user-interface-design)
- [3. References](#3-references)
### Document Revision History
| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2024-11-15 |Initial draft | 1.0 |
|Revision 2 |2025-2-11 | Second draft | 1.5 |


# 1. Introduction
The purpose of this document is to illustrate our plan for the website.

# 2. Software Design
(**Note**: For all subsections of Section-2: You should describe
the design for the end product (completed application) - not only
your iteration1 version. You will revise this document and add
more details later.)

## 2.1 Database Model
Provide a list of your tables (i.e., SQL Alchemy classes) in your
database model and briefly explain the role of each table.
Provide a UML diagram of your database model showing the
associations and relationships among tables.
The tables in our Model are: User, Student, Faculty, Position, Field, and Language. User is the table for all users. Student and Faculty are the tables to represent students and faculties. Position is used to represent the research positions from faculty that students can apply for. Field represents fields of research. Languages represent programming languages that are used in a project and that students can be proficient in.

## 2.2 Modules and Interfaces
### 2.2.1 Overview
Describe the high-level architecture of your software: i.e., the
major components/modules and how they fit together. Provide a UML
component diagram that illustrates the architecture of your
software. Briefly mention the role of each module in your
architectural design. Please refer to the "System Level Design"

Students are in fields; examples include Biotechnology and Computer Science. Positions each require fields, and Students apply for positions. Faculty make positions. There is no direct faculty-student link, each will just be associated with a related position. However, since students and faculty are very similar, they both inherit from a larger User class.

<kbd>
      <img src="images/uml_diagram.png"  border="2">
  </kbd>

### 2.2.2 Interfaces
Include a detailed description of the routes your application
will implement.
* Brainstorm with your team members and identify all routes you
need to implement for the **completed** application.
* For each route specify its , , and .
* You can use the following table template to list your route
specifications.
* Organize this section according to your module decomposition,
i.e., include a sub-section for each module and list all routes
for that sub-section in a table.
#### 2.2.2.1 \<Auth> Routes
| | Methods | URL Path | Description |
|:--|:------------------|:-----------|:-------------|
|1. |Get, Post |/faculty-register |Registers a faculty member into the database |
|2. |Get, Post |/student-register |Registers a student into the database |
|3. |Get, Post |/login |Used to login a user, so they can access the website |
|4. |Get |/logout |Used to logout a user |

#### 2.2.2.2 \<Main> Routes
| | Methods | URL Path | Description |
|:--|:------------------|:-----------|:-------------|
|1. | Get|/index |The main route where users can view projects. |
|2. |Get, Post |/create/position |Faculty create research positions |
|3. |Get, Post |/create/field |Faculty can create research fields |
|4. |Get, Post |/create/language |Faculty create languages |
|5. |Get, Post |/profile |Allows users to view their own profile, and faculty to accept or reject recommendations |
|6. |Get, Post |/profile/edit |Allows users to edit their own profile |
|7. |Post |/Apply |Allows a student to apply to positions |
|8. |Post |/withdraw | Allows a student to remove their application from submission|
|9. |Get, Post |/positions/faculty | allows faculty to see their positions and the students who have applied as well as accept or reject them.|
|10. |Get |/positions/student |allows student to see their accepted and applied to positions |

### 2.3 User Interface Design

See image “UI Mockup.jpg”
<kbd>
      <img src="images/UI Mockup.jpg"  border="2">
  </kbd>

# 3. References
Project Requirements Document, Sakire Aslan Ay
