const router = require('express').Router();
const { Grupo } = require('../db/models');

router.get('/', async (req, res) => {
  res.json(await Grupo.findAll({ order: [['grado', 'ASC'], ['nombre', 'ASC']] }));
});

router.post('/', async (req, res) => {
  const { nombre, grado, turno } = req.body;
  if (!nombre || !grado || !turno) return res.status(400).json({ error: 'Nombre, grado y turno son requeridos' });
  if (isNaN(grado)) return res.status(400).json({ error: 'Grado debe ser un número' });
  const grupo = await Grupo.create({ nombre, grado: parseInt(grado), turno });
  res.status(201).json(grupo);
});

router.put('/:id', async (req, res) => {
  const grupo = await Grupo.findByPk(req.params.id);
  if (!grupo) return res.status(404).json({ error: 'Grupo no encontrado' });
  const { nombre, grado, turno } = req.body;
  if (!nombre || !grado || !turno) return res.status(400).json({ error: 'Nombre, grado y turno son requeridos' });
  if (isNaN(grado)) return res.status(400).json({ error: 'Grado debe ser un número' });
  await grupo.update({ nombre, grado: parseInt(grado), turno });
  res.json(grupo);
});

router.delete('/:id', async (req, res) => {
  const grupo = await Grupo.findByPk(req.params.id);
  if (!grupo) return res.status(404).json({ error: 'Grupo no encontrado' });
  await grupo.destroy();
  res.json({ ok: true });
});

module.exports = router;
