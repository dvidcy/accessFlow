const router = require('express').Router();
const { Alumno, Grupo } = require('../db/models');

router.get('/', async (req, res) => {
  const where = req.query.grupo_id ? { grupo_id: req.query.grupo_id } : {};
  const alumnos = await Alumno.findAll({
    where,
    include: [{ model: Grupo }],
    order: [['nombre', 'ASC']],
  });
  res.json(alumnos);
});

router.post('/', async (req, res) => {
  const { nombre, grupo_id, rfid_uid } = req.body;
  if (!nombre || !grupo_id) return res.status(400).json({ error: 'Nombre y grupo son requeridos' });
  const alumno = await Alumno.create({ nombre, grupo_id, rfid_uid: rfid_uid || null });
  res.status(201).json(alumno);
});

router.put('/:id', async (req, res) => {
  const alumno = await Alumno.findByPk(req.params.id);
  if (!alumno) return res.status(404).json({ error: 'Alumno no encontrado' });
  const { nombre, grupo_id, rfid_uid } = req.body;
  if (!nombre || !grupo_id) return res.status(400).json({ error: 'Nombre y grupo son requeridos' });
  await alumno.update({ nombre, grupo_id, rfid_uid: rfid_uid || null });
  res.json(alumno);
});

router.delete('/:id', async (req, res) => {
  const alumno = await Alumno.findByPk(req.params.id);
  if (!alumno) return res.status(404).json({ error: 'Alumno no encontrado' });
  await alumno.destroy();
  res.json({ ok: true });
});

module.exports = router;
