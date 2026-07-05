import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Attendance from './pages/Attendance';
import Students from './pages/Students';
import Groups from './pages/Groups';
import Tutors from './pages/Tutors';
import Messaging from './pages/Messaging';

function PrivateRoute({ children }) {
  const { admin } = useAuth();
  return admin ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
            <Route index element={<Navigate to="/attendance" replace />} />
            <Route path="attendance" element={<Attendance />} />
            <Route path="students"   element={<Students />} />
            <Route path="groups"     element={<Groups />} />
            <Route path="tutors"     element={<Tutors />} />
            <Route path="messaging"  element={<Messaging />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
