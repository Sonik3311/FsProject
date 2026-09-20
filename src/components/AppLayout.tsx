import { NavLink, Outlet, useLocation } from 'react-router-dom'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Drawer from '@mui/material/Drawer'
import List from '@mui/material/List'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemText from '@mui/material/ListItemText'
import Box from '@mui/material/Box'

const NAV_ITEMS = [
  { to: '/dishes', label: 'Блюда (меню)' },
  { to: '/ingredients', label: 'Ингредиенты' },
  { to: '/allergens', label: 'Матрица аллергенов' },
  { to: '/labels', label: 'Этикетки' },
  { to: '/wastage', label: 'Списания' },
]

export function AppLayout() {
  const location = useLocation()

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Ассистент повара
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: 220,
          flexShrink: 0,
          '& .MuiDrawer-paper': { width: 220, boxSizing: 'border-box' },
        }}
      >
        <List>
          {NAV_ITEMS.map((item) => (
            <ListItemButton
              key={item.to}
              component={NavLink}
              to={item.to}
              selected={location.pathname.startsWith(item.to)}
            >
              <ListItemText primary={item.label} />
            </ListItemButton>
          ))}
        </List>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
        <Outlet />
      </Box>
    </Box>
  )
}