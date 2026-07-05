const nodemailer = require('nodemailer');

function getTransporter() {
  return nodemailer.createTransport({
    service: 'gmail',
    auth: { user: process.env.SMTP_EMAIL, pass: process.env.SMTP_PASSWORD },
  });
}

async function sendMail(to, subject, html) {
  try {
    await getTransporter().sendMail({
      from: process.env.SMTP_EMAIL,
      to,
      subject,
      html,
    });
    return true;
  } catch (e) {
    console.error(`[email] Error al enviar a ${to}:`, e.message);
    return false;
  }
}

async function notificarEntrada(email, nombre, hora) {
  return sendMail(
    email,
    `${nombre} llegó a la escuela`,
    `<p>Estimado tutor,</p><p><strong>${nombre}</strong> registró su <strong>entrada</strong> a las <strong>${hora}</strong>.</p><p>— AccessFlow</p>`
  );
}

async function notificarSalida(email, nombre, hora) {
  return sendMail(
    email,
    `${nombre} salió de la escuela`,
    `<p>Estimado tutor,</p><p><strong>${nombre}</strong> registró su <strong>salida</strong> a las <strong>${hora}</strong>.</p><p>— AccessFlow</p>`
  );
}

async function enviarMensajePersonalizado(email, asunto, cuerpo) {
  const html = `<p>${cuerpo.replace(/\n/g, '<br>')}</p><p>— AccessFlow</p>`;
  return sendMail(email, asunto, html);
}

module.exports = { notificarEntrada, notificarSalida, enviarMensajePersonalizado };
