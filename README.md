# Project Name

## Description

This project includes a runnable Node.js server with API endpoints to manage user authentication. The primary functionalities provided include user registration and login, leveraging MongoDB for data storage.

## API Endpoints

### Registration
- **POST /api/register**
  - Description: Registers a new user by taking username, email, and password, validates the request, checks for existing users, hashes the password, and stores the user in the database.
  - Parameters: `{ username, email, password }`
  - Returns: User object with status code 201 on success.
  
### Login
- **POST /api/login**
  - Description: Authenticates user credentials against the database. If authentication is successful, returns a success message (future implementations will handle JWT creation).
  - Parameters: `{ email, password }`
  - Returns: Success message with status code 200 on success.

### Hello
- **GET /api/hello**
  - Description: A simple API for testing that returns a hardcoded user object.
  - Parameters: None
  - Returns: A user object with status code 200.

## File Structure

The project is structured with a clear separation of concerns, mimicking a typical Node.js + Next.js application structure:

- `src/pages/api/` - Contains the API route implementations including `hello.js`, `login.js`, and `register.js`.
- `src/lib/` - Library code, including the MongoDB connection setup.
- `src/models/` - Mongoose models, includes a User model definition.
- `src/hooks/` - Custom React hooks for managing local storage and handling color theme changes.
- `src/components/` - Reusable React components.
  
## Key Components

- **MongoDB Integration (`src/lib/mongodb.js`)**
  - Responsible for database connection and management.
- **User Model (`src/models/User.js`)**
  - Defines the MongoDB schema for user data.
- **Authentication API (`src/pages/api/`)**
  - Includes all backend logic for handling authentication requests.
- **Custom Hooks (`src/hooks/`)**
  - Includes hooks for local storage management and UI theme settings.

In addition to these components, the project also includes basic configurations for Next.js (`next-env.d.ts`, and `tailwind.config.js`) which handle TypeScript support and Tailwind CSS configuration respectively.

For further details on file structure and more specific implementations, refer to the file structure logic implemented in the AST.js file[0].