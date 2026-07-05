const router = require('express').Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { Admin } = require('../db/models');

router.post('/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ error: 'Campos requeridos' });

  const admin = await Admin.findOne({ where: { email } });
  if (!admin || !(await bcrypt.compare(password, admin.password_hash))) {
    return res.status(401).json({ error: 'Credenciales incorrectas' });
  }

  const token = jwt.sign({ id: admin.id, email: admin.email }, process.env.JWT_SECRET, { expiresIn: '8h' });
  res.json({ token, admin: { id: admin.id, nombre: admin.nombre, email: admin.email } });
});

module.exports = router;
