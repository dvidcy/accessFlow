require('dotenv').config();
const bcrypt = require('bcrypt');
const { sequelize, Admin, Grupo, Alumno, Tutor, AlumnoTutor } = require('./models');

async function seed() {
  await sequelize.sync({ alter: true });

  const adminCount = await Admin.count();
  if (adminCount > 0) {
    console.log('La BD ya tiene datos, omitiendo seed.');
    await sequelize.close();
    return;
  }

  // Grupos
  const g1 = await Grupo.create({ nombre: '1A', grado: 1, turno: 'matutino' });
  const g2 = await Grupo.create({ nombre: '2B', grado: 2, turno: 'vespertino' });

  // Alumnos
  const alumnos = await Alumno.bulkCreate([
    { nombre: 'Carlos Méndez',  grupo_id: g1.id },
    { nombre: 'Sofía Ramos',    grupo_id: g1.id },
    { nombre: 'Luis Herrera',   grupo_id: g1.id },
    { nombre: 'Valeria Torres', grupo_id: g2.id },
    { nombre: 'Diego Morales',  grupo_id: g2.id },
  ]);

  // Tutores
  const t1 = await Tutor.create({ nombre: 'Ana Méndez',    email: 'ana@ejemplo.com',    telefono: '555-0001' });
  const t2 = await Tutor.create({ nombre: 'Roberto Ramos', email: 'roberto@ejemplo.com', telefono: '555-0002' });
  const t3 = await Tutor.create({ nombre: 'Lucía Torres',  email: 'lucia@ejemplo.com',  telefono: '555-0003' });

  // Relaciones alumno-tutor
  await AlumnoTutor.bulkCreate([
    { alumno_id: alumnos[0].id, tutor_id: t1.id, parentesco: 'madre' },
    { alumno_id: alumnos[0].id, tutor_id: t2.id, parentesco: 'padre' },
    { alumno_id: alumnos[1].id, tutor_id: t1.id, parentesco: 'madre' },
    { alumno_id: alumnos[2].id, tutor_id: t2.id, parentesco: 'padre' },
    { alumno_id: alumnos[3].id, tutor_id: t3.id, parentesco: 'madre' },
    { alumno_id: alumnos[4].id, tutor_id: t3.id, parentesco: 'madre' },
  ]);

  // Admin
  const hash = await bcrypt.hash('admin123', 10);
  await Admin.create({ nombre: 'Administrador', email: 'admin@accessflow.com', password_hash: hash });

  console.log('Seed completado:');
  console.log('  2 grupos, 5 alumnos, 3 tutores, 1 admin');
  console.log('  Admin → admin@accessflow.com / admin123');
  await sequelize.close();
}

seed().catch(err => { console.error(err); process.exit(1); });
