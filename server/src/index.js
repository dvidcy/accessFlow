require('dotenv').config();
const express = require('express');
const cors = require('cors');
const authMiddleware = require('./middleware/auth');

const app = express();
app.use(cors());
app.use(express.json());

app.use('/api/auth', require('./routes/auth'));
app.use('/api/attendance', authMiddleware, require('./routes/attendance'));
app.use('/api/students',   authMiddleware, require('./routes/students'));
app.use('/api/groups',     authMiddleware, require('./routes/groups'));
app.use('/api/tutors',     authMiddleware, require('./routes/tutors'));
app.use('/api/messaging',  authMiddleware, require('./routes/messaging'));

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`AccessFlow API → http://localhost:${PORT}`));
