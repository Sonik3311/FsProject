import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import type { Dish, Ingredient } from '../types'

interface LabelCardProps {
  dish: Dish
  ingredients: Ingredient[]
}

export function LabelCard({ dish, ingredients }: LabelCardProps) {
  const ids = new Set(dish.ingredients.map((d) => d.ingredientId))
  const allergens = [...new Set(ingredients.filter((i) => ids.has(i.id)).flatMap((i) => i.allergens))]

  return (
    <Card variant="outlined" sx={{ width: 300, p: 2 }}>
      <CardContent>
        <Typography variant="h6" align="center">
          {dish.name}
        </Typography>
        <Divider sx={{ my: 1 }} />
        <Typography variant="body2" color="text.secondary">
          Аллергены: {allergens.join(', ') || 'нет'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Дата: {new Date().toLocaleDateString('ru-RU')}
        </Typography>
      </CardContent>
    </Card>
  )
}