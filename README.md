# FastAPI Music Player Backend

## Overview

This repository contains the backend for the Music Player application built with FastAPI. The backend handles audio file uploads, retrieves audio records, and integrates with Cloudinary for file storage. It also uses asynchronous operations with PostgreSQL and includes CORS middleware for security.

## Endpoints

### Upload Audio

- **Endpoint:** `/upload`
- **Method:** `POST`
- **Description:** Uploads an audio file along with track name and author name.
- **Form Data:**
  - `track_name`: Name of the track (string, required)
  - `author_name`: Name of the author (string, required)
  - `file`: Audio file (MP3, required)
- **Response:**
  - `id`: ID of the audio record
  - `url`: URL of the uploaded audio file on Cloudinary
  - `track_name`: Name of the track
  - `author_name`: Name of the author

### Get Audio Tracks

- **Endpoint:** `/tracks`
- **Method:** `GET`
- **Description:** Retrieves all audio records from the database.
- **Response:**
  - A list of audio records with `id`, `url`, `track_name`, and `author_name`.

## Technologies Used

- **FastAPI:** Modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Asyncpg:** PostgreSQL driver for asynchronous operations.
- **SQLAlchemy:** SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Cloudinary:** Media management platform for storing and serving audio files.
- **CORS Middleware:** Configured to allow specific origins for cross-origin requests.

## Frontend Integration

This backend service is integrated with the front-end project, which is deployed at [Music Player UI](https://music-player-ui-ux.vercel.app/) and its repository is available [here](https://github.com/osamaaslam86004/Music-Player.git).

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn main:app --reload
   ```


