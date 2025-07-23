// express_mongo_app/server.js

const express = require('express');
const { MongoClient } = require('mongodb');
const dotenv = require('dotenv');
const cors = require('cors');

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;
const mongoUri = process.env.MONGO_URI || "mongodb://localhost:27017";
const dbName = "dealership_db";

app.use(cors());
app.use(express.json());

let db;

async function connectToMongo() {
    try {
        const client = new MongoClient(mongoUri, { useNewUrlParser: true, useUnifiedTopology: true });
        await client.connect();
        db = client.db(dbName);
        console.log("Connected to MongoDB");
    } catch (error) {
        console.error("Failed to connect to MongoDB:", error);
        process.exit(1);
    }
}

// Routes

// To fetch all dealers [cite: 101]
app.get('/fetchDealers', async (req, res) => {
    try {
        const dealers = await db.collection('dealerships').find({}).toArray();
        res.json(dealers);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// To fetch dealer by id [cite: 102]
app.get('/fetchDealer/:id', async (req, res) => {
    try {
        const dealerId = parseInt(req.params.id);
        const dealer = await db.collection('dealerships').findOne({ id: dealerId });
        if (dealer) {
            res.json(dealer);
        } else {
            res.status(404).json({ message: 'Dealer not found' });
        }
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// To fetch all reviews [cite: 103]
app.get('/fetchReviews', async (req, res) => {
    try {
        const reviews = await db.collection('reviews').find({}).toArray();
        res.json(reviews);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// To fetch reviews for a dealer by id [cite: 104]
app.get('/fetchReview/dealer/:id', async (req, res) => {
    try {
        const dealerId = parseInt(req.params.id);
        const reviews = await db.collection('reviews').find({ dealership: dealerId }).toArray();
        res.json(reviews); // 
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

app.get('/fetchDealers/:state', async (req, res) => {
  const state = req.params.state;
  const dealers = await db.collection('dealerships').find({ state }).toArray();
  res.json(dealers);
});

// To insert a review [cite: 105]
app.post('/insertReview', async (req, res) => {
    try {
        const newReview = req.body;
        newReview.time = new Date(); // Set current time [cite: 185]
        const result = await db.collection('reviews').insertOne(newReview);
        res.status(201).json(result.ops[0]);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// Dummy data for initial testing if MongoDB isn't populated yet
// In a real scenario, you'd populate your MongoDB with actual data.
async function populateDummyData() {
    const dealersCollection = db.collection('dealerships');
    const reviewsCollection = db.collection('reviews');

    const dealerCount = await dealersCollection.countDocuments();
    const reviewCount = await reviewsCollection.countDocuments();

    if (dealerCount === 0) {
        console.log("Populating dummy dealer data...");
        await dealersCollection.insertMany([
            { id: 1, name: "Best Cars NYC", address: "123 Broadway, New York, NY", state: "NY" },
            { id: 2, name: "Luxury Motors CA", address: "456 Sunset Blvd, Los Angeles, CA", state: "CA" },
            { id: 3, name: "Kansas Auto", address: "789 Main St, Wichita, KS", state: "KS" },
            { id: 4, name: "Texas Trucks", address: "101 Rodeo Dr, Dallas, TX", state: "TX" },
        ]);
    }

    if (reviewCount === 0) {
        console.log("Populating dummy review data...");
        await reviewsCollection.insertMany([
            { dealership: 1, user_id: 1, name: "John Doe", review: "Great service!", time: new Date(), purchase: true, purchase_date: "01/01/2023", car_make: "Toyota", car_model: "Camry", car_year: 2020 },
            { dealership: 1, user_id: 2, name: "Jane Smith", review: "Friendly staff.", time: new Date(), purchase: false },
            { dealership: 3, user_id: 3, name: "Alice Brown", review: "Found my dream car here!", time: new Date(), purchase: true, purchase_date: "03/15/2024", car_make: "Ford", car_model: "F-150", car_year: 2023 },
        ]);
    }
}

// 🔻 Tambahkan ini sebelum listen!
app.get('/', (req, res) => {
  res.send('🚗 Car Dealership backend is running!');
});

app.listen(port, async () => {
    await connectToMongo();
    await populateDummyData(); // Populate data after connection
    console.log(`Express-Mongo app listening at http://localhost:${port}`);
});