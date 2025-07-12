import React from 'react';
import {
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Paper,
  Typography,
  Slider,
  Switch,
  FormControlLabel,
} from '@mui/material';
import { SearchOutlined, FilterListOutlined } from '@mui/icons-material';
import { motion } from 'framer-motion';

const SkillFilters = ({
  searchTerm,
  setSearchTerm,
  category,
  setCategory,
  level,
  setLevel,
  sortBy,
  setSortBy,
  showAdvanced,
  setShowAdvanced,
}) => {
  const categories = [
    { value: 'all', label: 'All Categories' },
    { value: 'programming', label: 'Programming' },
    { value: 'design', label: 'Design' },
    { value: 'marketing', label: 'Marketing' },
    { value: 'languages', label: 'Languages' },
    { value: 'music', label: 'Music' },
    { value: 'cooking', label: 'Cooking' },
    { value: 'other', label: 'Other' },
  ];

  const levels = [
    { value: 'all', label: 'All Levels' },
    { value: 'beginner', label: 'Beginner' },
    { value: 'intermediate', label: 'Intermediate' },
    { value: 'advanced', label: 'Advanced' },
    { value: 'expert', label: 'Expert' },
  ];

  const sortOptions = [
    { value: 'newest', label: 'Newest First' },
    { value: 'oldest', label: 'Oldest First' },
    { value: 'name', label: 'Name A-Z' },
    { value: 'category', label: 'Category' },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Paper
        elevation={2}
        sx={{
          p: 3,
          mb: 3,
          background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        }}
      >
        <Box display="flex" alignItems="center" gap={1} mb={2}>
          <FilterListOutlined color="primary" />
          <Typography variant="h6" color="primary">
            Find Your Perfect Skill
          </Typography>
        </Box>

        <Box display="flex" gap={2} flexWrap="wrap" alignItems="center">
          <TextField
            placeholder="Search skills, descriptions, or teachers..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: <SearchOutlined sx={{ mr: 1, color: 'text.secondary' }} />,
            }}
            sx={{ minWidth: 300, flexGrow: 1 }}
            size="small"
          />

          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Category</InputLabel>
            <Select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              label="Category"
            >
              {categories.map((cat) => (
                <MenuItem key={cat.value} value={cat.value}>
                  {cat.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Level</InputLabel>
            <Select
              value={level}
              onChange={(e) => setLevel(e.target.value)}
              label="Level"
            >
              {levels.map((lvl) => (
                <MenuItem key={lvl.value} value={lvl.value}>
                  {lvl.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ minWidth: 140 }}>
            <InputLabel>Sort By</InputLabel>
            <Select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              label="Sort By"
            >
              {sortOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>

        <Box mt={2}>
          <FormControlLabel
            control={
              <Switch
                checked={showAdvanced}
                onChange={(e) => setShowAdvanced(e.target.checked)}
                color="primary"
              />
            }
            label="Advanced Filters"
          />
        </Box>

        {showAdvanced && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Box mt={2} p={2} bgcolor="background.paper" borderRadius={2}>
              <Typography variant="subtitle2" gutterBottom>
                Additional Filters
              </Typography>
              <Box display="flex" gap={2} flexWrap="wrap">
                <Chip label="Recently Added" variant="outlined" clickable />
                <Chip label="Highly Rated" variant="outlined" clickable />
                <Chip label="Quick to Learn" variant="outlined" clickable />
                <Chip label="In-Person Available" variant="outlined" clickable />
              </Box>
            </Box>
          </motion.div>
        )}
      </Paper>
    </motion.div>
  );
};

export default SkillFilters;