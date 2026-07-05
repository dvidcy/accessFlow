const router = require('express').Router();
const { Tutor, Alumno, Grupo, Mensaje, MensajeDestinatario } = require('../db/models');
const { enviarMensajePersonalizado } = require('../services/email');

router.post('/send', async (req, res) => {
  const { tipo, tutor_id, grupo_id, asunto, cuerpo } = req.body;
  const admin_id = req.admin.id;

  if (!asunto || !cuerpo) return res.status(400).json({ error: 'Asunto y mensaje son requeridos' });

  let tutores = [];

  if (tipo === 'individual') {
    if (!tutor_id) return res.status(400).json({ error: 'Selecciona un tutor' });
    const tutor = await Tutor.findByPk(tutor_id);
    if (!tutor) return res.status(404).json({ error: 'Tutor no encontrado' });
    tutores = [tutor];
  } else if (tipo === 'grupal') {
    if (!grupo_id) return res.status(400).json({ error: 'Selecciona un grupo' });
    const alumnos = await Alumno.findAll({ where: { grupo_id }, include: [Tutor] });
    const seen = new Set();
    for (const a of alumnos) {
      for (const t of a.Tutores) {
        if (!seen.has(t.id)) { seen.add(t.id); tutores.push(t); }
      }
    }
    if (!tutores.length) return res.status(400).json({ error: 'El grupo no tiene tutores registrados' });
  } else {
    return res.status(400).json({ error: 'Tipo inválido' });
  }

  const mensaje = await Mensaje.create({ admin_id, asunto, cuerpo, tipo });
  await MensajeDestinatario.bulkCreate(tutores.map(t => ({ mensaje_id: mensaje.id, tutor_id: t.id })));

  let enviados = 0;
  for (const t of tutores) {
    if (await enviarMensajePersonalizado(t.email, asunto, cuerpo)) enviados++;
  }

  res.json({ ok: true, destinatarios: tutores.length, enviados });
});

module.exports = router;
