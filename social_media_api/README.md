# Social Media API Project

This is a social media API project built using Django REST Framework (DRF) that supports core features such as friendship management, posting content, and real-time group chat. The project is containerized using Docker and requires some initial configuration steps for setup.

## Features

### Friendship Management

This API allows users to manage friendships with other users, including:

- **Send Friend Request**: Send a request to another user to establish a friendship.
- **Accept Friend Request**: Accept a pending friend request from another user.
- **Reject Friend Request**: Decline a pending friend request.
- **Remove Friend**: Remove an existing friend from your friends list.
- **List Friends**: View a list of all friends.
- **List Pending Requests**: See a list of all pending friend requests sent or received.

### Posts

Users can manage their posts, including:

- **Create a Post**: Users can create a new post by providing text, images, or other media.
- **Delete a Post**: Users can delete their own posts.
- **Update a Post**: Modify an existing post.
- **List Posts**: Retrieve a list of posts, either for a specific user or all posts.

### Real-time Group Chat

This feature allows users to engage in real-time group chats using WebSockets. Key features include:

- **Create a Group**: Users can create a chat group.
- **Join a Group**: Users can join an existing chat group.
- **Send Messages**: Send real-time messages to the group using WebSockets.
- **Receive Messages**: Receive and display messages in real-time as they are sent.
- **List Group Messages**: Retrieve the chat history for a particular group.

### Authentication and User Management

- **User Registration**: Allow new users to sign up.
- **User Login**: Enable existing users to log in and get authenticated.
- **User Profile**: View and edit user profile information.

## Installation and Setup

### Requirements

- Docker
- Docker Compose

### Environment Variables

Before starting the project, ensure that you have the following environment files ready:

- `.env/local`: This file should contain local environment variables for development.
- `.env/production`: This file should contain environment variables for the production environment.



### Steps to Run Locally

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/AhmedNagi1/Social_Media_Api.git
   cd Social_Media_Api
   ```
2. **Set Up Environment Variables**:
   Make sure to copy the `.env/.local` or `.env/.production` files into the `.envs` directory and update them with your configurations.
Here's an updated version of the **3. Build and Run Docker Containers** section in English with the differentiation between development and production environments:

---

### 3. **Build and Run Docker Containers**


- **For Development Environment**:
   If you're running the project locally in a development environment, use the `docker-compose.local.yml` file to ensure the settings are tailored for local development.

   **Command for development**:
   ```bash
   docker-compose -f docker-compose.local.yml up --build
   ```

- **For Production Environment**:
   If you're deploying the project in a production environment, use the `docker-compose.production.yml` file to configure production-ready settings such as optimized performance and security.

   **Command for production**:
   ```bash
   docker-compose -f docker-compose.production.yml up --build
   ```

--- 

### Additional Notes

- **Media Files**: Uploaded posts (e.g., images) are stored in the `media/` directory.
- **Static Files**: Static assets (JavaScript, CSS) are stored in the `staticfiles/` directory.
- **Real-time Features**: Real-time group chat functionality relies on WebSockets and Redis as a message broker.
