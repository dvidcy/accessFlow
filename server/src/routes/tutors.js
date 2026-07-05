const router = require('express').Router();
const { Tutor, Alumno, AlumnoTutor } = require('../db/models');

router.get('/', async (req, res) => {
  const tutores = await Tutor.findAll({
    include: [{ model: Alumno }],
    order: [['nombre', 'ASC']],
  });
  res.json(tutores);
});

router.post('/', async (req, res) => {
  const { nombre, email, telefono, alumno_id, parentesco } = req.body;
  if (!nombre || !email) return res.status(400).json({ error: 'Nombre y email son requeridos' });
  const tutor = await Tutor.create({ nombre, email, telefono: telefono || null });
  if (alumno_id) {
    await AlumnoTutor.create({ alumno_id, tutor_id: tutor.id, parentesco: parentesco || null });
  }
  res.status(201).json(tutor);
});

router.put('/:id', async (req, res) => {
  const tutor = await Tutor.findByPk(req.params.id);
  if (!tutor) return res.status(404).json({ error: 'Tutor no encontrado' });
  const { nombre, email, telefono } = req.body;
  if (!nombre || !email) return res.status(400).json({ error: 'Nombre y email son requeridos' });
  await tutor.update({ nombre, email, telefono: telefono || null });
  res.json(tutor);
});

router.delete('/:id', async (req, res) => {
  const tutor = await Tutor.findByPk(req.params.id);
  if (!tutor) return res.status(404).json({ error: 'Tutor no encontrado' });
  await tutor.destroy();
  res.json({ ok: true });
});

module.exports = router;
