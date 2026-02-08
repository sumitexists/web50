# CS50 Web – Project 2: Commerce

An eBay-like auction website built using **Django**, allowing users to create listings, place bids, manage watchlists, and comment on auctions.

This project is part of **CS50’s Web Programming with Python and JavaScript**.

---

## Features

### Authentication
- User registration
- Login & logout
- Access control for authenticated actions

### Listings
- Create new auction listings
- View all active listings
- View individual listing pages
- Close auction (only by listing owner)

### Bidding System
- Users can place bids on active listings
- Bid must be higher than the current highest bid
- Winning bidder is displayed after auction is closed

### Watchlist
- Users can add or remove listings from their watchlist
- Dedicated watchlist page for each user

### Comments
- Authenticated users can comment on listings
- Comments are displayed in chronological order

### Categories
- Listings are categorized
- Users can filter listings by category

---

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Bootstrap)
- **Database:** SQLite
- **Authentication:** Django built-in auth system

---

## Forms Handling (Important Note)

⚠️ **Django Forms were NOT used in this project**

- All forms are implemented using **plain HTML**
- Data is processed manually via `request.POST`
- Validation is handled explicitly in views
- This approach was chosen to gain a deeper understanding of:
  - HTTP POST requests
  - Form validation logic
  - Django request/response cycle

---

## Models Overview

- **User** (Django default)
- **Listing**
  - title, description, starting bid, image URL, category
  - owner (ForeignKey → User)
  - active status
- **Bid**
  - bid amount
  - bidder (ForeignKey → User)
  - related listing
- **Comment**
  - comment text
  - author (ForeignKey → User)
  - related listing
- **Watchlist**
  - Many-to-Many relationship between User and Listing

---

## How to Run the Project

1. Clone the repository
   ```bash
   git clone <repository-url>
