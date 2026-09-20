import { Link } from 'react-router-dom'
import Card from '@mui/material/Card'
import CardActionArea from '@mui/material/CardActionArea'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import Chip from '@mui/material/Chip'
import Box from '@mui/material/Box'
import Divider from '@mui/material/Divider'
import type { Dish, Ingredient } from '../types'

interface DishCardProps {
  dish: Dish
  ingredients: Ingredient[]
}

function dishCost(dish: Dish, ingredients: Ingredient[]): number {
  const byId = new Map(ingredients.map((i) => [i.id, i]))
  return dish.ingredients.reduce((sum, di) => {
    const ing = byId.get(di.ingredientId)
    return sum + (ing ? ing.pricePerUnit * di.qty : 0)
  }, 0)
}

function dishAllergens(dish: Dish, ingredients: Ingredient[]): string[] {
  const ids = new Set(dish.ingredients.map((d) => d.ingredientId))
  return [...new Set(ingredients.filter((i) => ids.has(i.id)).flatMap((i) => i.allergens))]
}

export function DishCard({ dish, ingredients }: DishCardProps) {
  const cost = dishCost(dish, ingredients)
  const allergens = dishAllergens(dish, ingredients)

  return (
    <Card
      elevation={0}
      sx={{
        width: { xs: '100%', sm: 300 },
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'background.paper',
        border: 1,
        borderColor: 'grey.400',
        boxShadow: '0 4px 12px rgba(0,0,0,0.25)',
      }}
    >
      <CardActionArea>
        <Link to={`/dishes/${dish.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              {dish.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Ингредиентов: {dish.ingredients.length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Себестоимость: {cost.toFixed(2)} ₽
            </Typography>
            <Divider sx={{ my: 1 }} />
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {allergens.length === 0 ? (
                <Chip label="Без аллергенов" size="small" />
              ) : (
                allergens.map((a) => <Chip key={a} label={a} size="small" />)
              )}
            </Box>
          </CardContent>
        </Link>
      </CardActionArea>
    </Card>
  )
}