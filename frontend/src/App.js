import { Route, Routes, Navigate } from 'react-router-dom';
import Login from './views/Login'
import Register from './views/Register'
import Layout from './components/Layout'

function App() {
  return (
    <>
          <Routes>
              <Route path="/" element={<Layout/>}>
                  <Route path="login" element={<Login />} />
                  <Route path="register" element={<Register />} />

              </Route>
              <Route path="*" element={<Navigate replace to="/login" />} />
          </Routes>
    </>
);
}

export default App;
