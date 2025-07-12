import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Chip,
  Button,
  Avatar,
  Box,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  PersonOutlined,
  CalendarTodayOutlined,
  StarOutlined,
  FavoriteOutlined,
  ShareOutlined,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

const SkillCard = ({ skill, onRequest, showActions = true }) => {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const getCategoryColor = (category) => {
    const colors = {
      programming: 'primary',
      design: 'secondary',
      marketing: 'success',
      languages: 'warning',
      music: 'info',
      cooking: 'error',
      other: 'default',
    };
    return colors[category] || 'default';
  };

  const getLevelColor = (level) => {
    const colors = {
      beginner: 'success',
      intermediate: 'warning',
      advanced: 'error',
      expert: 'secondary',
    };
    return colors[level] || 'default';
  };

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -4 }}
    >
      <Card
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          transition: 'all 0.3s ease-in-out',
          '&:hover': {
            boxShadow: 6,
            transform: 'translateY(-2px)',
          },
        }}
      >
        <CardContent sx={{ flexGrow: 1 }}>
          <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
            <Typography variant="h6" component="h3" gutterBottom>
              {skill.name}
            </Typography>
            <Box display="flex" gap={0.5}>
              <Tooltip title="Add to favorites">
                <IconButton size="small">
                  <FavoriteOutlined fontSize="small" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Share skill">
                <IconButton size="small">
                  <ShareOutlined fontSize="small" />
                </IconButton>
              </Tooltip>
            </Box>
          </Box>

          <Typography
            variant="body2"
            color="text.secondary"
            paragraph
            sx={{
              display: '-webkit-box',
              WebkitLineClamp: 3,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
            }}
          >
            {skill.description}
          </Typography>

          <Box display="flex" gap={1} mb={2} flexWrap="wrap">
            <Chip
              label={skill.category}
              color={getCategoryColor(skill.category)}
              size="small"
              variant="outlined"
            />
            <Chip
              label={skill.level}
              color={getLevelColor(skill.level)}
              size="small"
            />
          </Box>

          <Box display="flex" alignItems="center" gap={1} mb={1}>
            <Avatar
              sx={{
                width: 24,
                height: 24,
                fontSize: '0.75rem',
                bgcolor: 'primary.main',
              }}
            >
              {skill.owner?.name?.charAt(0).toUpperCase()}
            </Avatar>
            <Typography variant="body2" color="text.secondary">
              {skill.owner?.name}
            </Typography>
          </Box>

          <Box display="flex" alignItems="center" gap={1}>
            <CalendarTodayOutlined sx={{ fontSize: 16, color: 'text.secondary' }} />
            <Typography variant="caption" color="text.secondary">
              {new Date(skill.created_at).toLocaleDateString()}
            </Typography>
          </Box>
        </CardContent>

        {showActions && (
          <CardActions sx={{ p: 2, pt: 0 }}>
            <Button
              variant="contained"
              fullWidth
              onClick={() => onRequest(skill.id)}
              sx={{
                background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #5a6fd8 30%, #6a4190 90%)',
                },
              }}
            >
              Request to Learn
            </Button>
          </CardActions>
        )}
      </Card>
    </motion.div>
  );
};

export default SkillCard;