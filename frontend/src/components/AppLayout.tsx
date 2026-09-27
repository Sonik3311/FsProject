import { useState } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import IconButton from '@mui/material/IconButton'
import MenuIcon from '@mui/icons-material/Menu'
import Drawer from '@mui/material/Drawer'
import List from '@mui/material/List'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemText from '@mui/material/ListItemText'
import Box from '@mui/material/Box'
import useMediaQuery from '@mui/material/useMediaQuery'

const NAV_ITEMS = [
  { to: '/dishes', label: 'Блюда (меню)' },
  { to: '/ingredients', label: 'Ингредиенты' },
  { to: '/allergens', label: 'Матрица аллергенов' },
  { to: '/labels', label: 'Этикетки' },
  { to: '/wastage', label: 'Списания' },
]

const DRAWER_WIDTH = 220

function NavList() {
  const location = useLocation()
  return (
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
  )
}

export function AppLayout() {
  const isDesktop = useMediaQuery(`(min-width: 900px)`)
  const [drawerOpen, setDrawerOpen] = useState(false)

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          {!isDesktop && (
            <IconButton
              edge="start"
              color="inherit"
              aria-label="Меню"
              onClick={() => setDrawerOpen(true)}
            >
              <MenuIcon />
            </IconButton>
          )}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Ассистент повара
          </Typography>
        </Toolbar>
      </AppBar>

      {isDesktop ? (
        <Drawer
          variant="permanent"
          open
          sx={{
            width: DRAWER_WIDTH,
            flexShrink: 0,
            '& .MuiDrawer-paper': { width: DRAWER_WIDTH, boxSizing: 'border-box' },
          }}
        >
          <NavList />
        </Drawer>
      ) : (
        <Drawer
          variant="temporary"
          open={drawerOpen}
          onClose={() => setDrawerOpen(false)}
          sx={{ '& .MuiDrawer-paper': { width: DRAWER_WIDTH, boxSizing: 'border-box' } }}
        >
          <NavList />
        </Drawer>
      )}

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          px: { xs: 1, sm: 2, md: 3 },
          py: { xs: 2, md: 3 },
          mt: 8,
          bgcolor: 'grey.100',
          minHeight: '100vh',
        }}
      >
        <Outlet />
      </Box>
    </Box>
  )
}