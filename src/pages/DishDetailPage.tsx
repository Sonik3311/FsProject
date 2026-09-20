import { useParams, Link } from 'react-router-dom'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Chip from '@mui/material/Chip'
import { dishes, ingredients } from '../data/mock'
import type { Dish } from '../types'

function dishCost(dish: Dish): number {
  const byId = new Map(ingredients.map((i) => [i.id, i]))
  return dish.ingredients.reduce((sum, di) => {
    const ing = byId.get(di.ingredientId)
    return sum + (ing ? ing.pricePerUnit * di.qty : 0)
  }, 0)
}

export function DishDetailPage() {
  const { id } = useParams()
  const dish = dishes.find((d) => d.id === Number(id))
  const byId = new Map(ingredients.map((i) => [i.id, i]))

  if (!dish) {
    return (
      <Typography variant="h6" color="error">
        Блюдо не найдено
      </Typography>
    )
  }

  return (
    <Box>
      <Button component={Link} to="/dishes">
        К списку блюд
      </Button>
      <Typography variant="h5">{dish.name}</Typography>
      <Typography variant="subtitle1">Себестоимость: {dishCost(dish).toFixed(2)} ₽</Typography>

      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Ингредиент</TableCell>
            <TableCell>Количество</TableCell>
            <TableCell>Стоимость</TableCell>
            <TableCell>Аллергены</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {dish.ingredients.map((di) => {
            const ing = byId.get(di.ingredientId)
            return (
              <TableRow key={di.ingredientId}>
                <TableCell>{ing?.name ?? '?'}</TableCell>
                <TableCell>{di.qty} {ing?.unit}</TableCell>
                <TableCell>{(ing?.pricePerUnit ?? 0) * di.qty} ₽</TableCell>
                <TableCell>
                  {ing?.allergens.map((a) => <Chip key={a} label={a} size="small" />)}
                </TableCell>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </Box>
  )
}