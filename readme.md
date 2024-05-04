# Project README.md

## Overview
This repository contains the codebase for a web application developed with Next.js and MongoDB, utilizing TypeScript and TailwindCSS for styling.

## Key Components and Their Interactions
1. **Custom Hooks**: `useLocalStorage` and `useColorMode` are hooks designed for managing local storage data and UI color mode respectively[0].
2. **API Routes**: Handlers for `register`, `login`, and a sample `hello` API route which are crucial for user management and backend functionality [1].
3. **Model**: The `User` Model using Mongoose for MongoDB interactions.
4. **Database Configuration**: `dbConnect` function facilitates connection handling with MongoDB server using environment configurations[2].

## API Calls (Backend)
- **Login API**: Handles POST requests to authenticate users using email and password. It includes error handling for cases like user not found or invalid credentials[1].
- **Register API**: Handles POST requests for user registration, handling the logic for duplicate user check and password hashing before storing the user data[1].
- **Hello API**: A simple GET API that returns a static response. This is generally used as a test API[1].

## File Structure
The application's file structure is generated and logged using the `AST.js` script, which organizes files and directories while excluding node_modules and specific config folders like `.next` and `.git`[6]:
- **src/pages**: Contains the React components for the pages of the application.
- **src/models**: Houses the Mongoose models used to interact with MongoDB.
- **src/lib**: Includes library functions such as the MongoDB connection helper.
- **src/hooks**: Custom React hooks like `useLocalStorage`.
- **src/components**: Reusable React components across the application.

## How to Set Up and Run the Project

1. **Environment Setup**: Ensure MongoDB URI is set in your `.env` file as `MONGODB_URI`.
2. **Install Dependencies**:
   ```bash
   npm install
   ```
3. **Run the Development Server**:
   ```bash
   npm run dev
   ```