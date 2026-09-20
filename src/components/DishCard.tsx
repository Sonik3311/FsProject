import { Link } from 'react-router-dom'
import Card from '@mui/material/Card'
import CardActionArea from '@mui/material/CardActionArea'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import type { Dish } from '../types'

interface DishCardProps {
  dish: Dish
}

export function DishCard({ dish }: DishCardProps) {
  return (
    <Card variant="outlined">
      <CardActionArea>
        <Link to={`/dishes/${dish.id}`}>
          <CardContent>
            <Typography variant="h6">{dish.name}</Typography>
            <Typography variant="body2" color="text.secondary">
              Ингредиентов: {dish.ingredients.length}
            </Typography>
          </CardContent>
        </Link>
      </CardActionArea>
    </Card>
  )
}