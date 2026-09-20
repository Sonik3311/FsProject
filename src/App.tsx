import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AppLayout } from './components/AppLayout'
import { DishesPage } from './pages/DishesPage'
import { DishDetailPage } from './pages/DishDetailPage'
import { IngredientsPage } from './pages/IngredientsPage'
import { AllergensPage } from './pages/AllergensPage'
import { LabelsPage } from './pages/LabelsPage'
import { WastagePage } from './pages/WastagePage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<Navigate to="/dishes" replace />} />
          <Route path="/dishes" element={<DishesPage />} />
          <Route path="/dishes/:id" element={<DishDetailPage />} />
          <Route path="/ingredients" element={<IngredientsPage />} />
          <Route path="/allergens" element={<AllergensPage />} />
          <Route path="/labels" element={<LabelsPage />} />
          <Route path="/wastage" element={<WastagePage />} />
          <Route path="*" element={<Navigate to="/dishes" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App