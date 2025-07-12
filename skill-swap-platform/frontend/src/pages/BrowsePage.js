import React, { useState, useEffect, useMemo } from 'react';
import {
  Container,
  Typography,
  Grid,
  Box,
  Pagination,
  Fab,
  Zoom,
  Alert,
} from '@mui/material';
import { FilterListOutlined } from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { useAuth } from '../context/AuthContext';
import SkillCard from '../components/Skills/SkillCard';
import SkillFilters from '../components/Skills/SkillFilters';
import LoadingSpinner from '../components/UI/LoadingSpinner';
import ErrorBoundary from '../components/UI/ErrorBoundary';

const BrowsePage = () => {
  const { api, user } = useAuth();
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('all');
  const [level, setLevel] = useState('all');
  const [sortBy, setSortBy] = useState('newest');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [page, setPage] = useState(1);
  const [showFilters, setShowFilters] = useState(true);
  const skillsPerPage = 12;

  const {
    data: skills = [],
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ['skills'],
    queryFn: async () => {
      const response = await api.get('/api/skills');
      return response.data.filter(skill => skill.owner_id !== user?.id);
    },
    staleTime: 5 * 60 * 1000,
  });

  const filteredAndSortedSkills = useMemo(() => {
    let filtered = skills.filter(skill => {
      const matchesSearch = 
        skill.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        skill.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        skill.owner?.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = category === 'all' || skill.category === category;
      const matchesLevel = level === 'all' || skill.level === level;
      return matchesSearch && matchesCategory && matchesLevel;
    });

    // Sort skills
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return new Date(b.created_at) - new Date(a.created_at);
        case 'oldest':
          return new Date(a.created_at) - new Date(b.created_at);
        case 'name':
          return a.name.localeCompare(b.name);
        case 'category':
          return a.category.localeCompare(b.category);
        default:
          return 0;
      }
    });

    return filtered;
  }, [skills, searchTerm, category, level, sortBy]);

  const paginatedSkills = useMemo(() => {
    const startIndex = (page - 1) * skillsPerPage;
    return filteredAndSortedSkills.slice(startIndex, startIndex + skillsPerPage);
  }, [filteredAndSortedSkills, page]);

  const totalPages = Math.ceil(filteredAndSortedSkills.length / skillsPerPage);

  const handleRequestSkill = async (skillId) => {
    try {
      await api.post('/api/requests', {
        skillId,
        message: 'I would like to learn this skill!'
      });
      toast.success('Request sent successfully!');
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Failed to send request';
      toast.error(errorMessage);
    }
  };

  const handlePageChange = (event, newPage) => {
    setPage(newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to load skills. Please try again.
        </Alert>
      </Container>
    );
  }

  return (
    <ErrorBoundary>
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Typography
            variant="h3"
            component="h1"
            gutterBottom
            sx={{
              fontWeight: 700,
              textAlign: 'center',
              mb: 4,
              background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Discover Amazing Skills
          </Typography>
        </motion.div>

        <AnimatePresence>
          {showFilters && (
            <SkillFilters
              searchTerm={searchTerm}
              setSearchTerm={setSearchTerm}
              category={category}
              setCategory={setCategory}
              level={level}
              setLevel={setLevel}
              sortBy={sortBy}
              setSortBy={setSortBy}
              showAdvanced={showAdvanced}
              setShowAdvanced={setShowAdvanced}
            />
          )}
        </AnimatePresence>

        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h6" color="text.secondary">
            {filteredAndSortedSkills.length} skill{filteredAndSortedSkills.length !== 1 ? 's' : ''} found
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Page {page} of {totalPages}
          </Typography>
        </Box>

        {isLoading ? (
          <LoadingSpinner message="Loading amazing skills..." />
        ) : filteredAndSortedSkills.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <Box
              display="flex"
              flexDirection="column"
              alignItems="center"
              justifyContent="center"
              minHeight="400px"
              textAlign="center"
            >
              <Typography variant="h4" gutterBottom color="text.secondary">
                🔍 No Skills Found
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                {skills.length === 0
                  ? "No skills available yet. Be the first to add a skill!"
                  : "Try adjusting your search criteria or filters."}
              </Typography>
            </Box>
          </motion.div>
        ) : (
          <>
            <Grid container spacing={3}>
              <AnimatePresence>
                {paginatedSkills.map((skill, index) => (
                  <Grid item xs={12} sm={6} md={4} key={skill.id}>
                    <motion.div
                      layout
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                    >
                      <SkillCard
                        skill={skill}
                        onRequest={handleRequestSkill}
                        showActions={true}
                      />
                    </motion.div>
                  </Grid>
                ))}
              </AnimatePresence>
            </Grid>

            {totalPages > 1 && (
              <Box display="flex" justifyContent="center" mt={6}>
                <Pagination
                  count={totalPages}
                  page={page}
                  onChange={handlePageChange}
                  color="primary"
                  size="large"
                  showFirstButton
                  showLastButton
                />
              </Box>
            )}
          </>
        )}

        <Zoom in={!showFilters}>
          <Fab
            color="primary"
            aria-label="show filters"
            onClick={() => setShowFilters(true)}
            sx={{
              position: 'fixed',
              bottom: 16,
              right: 16,
              background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
            }}
          >
            <FilterListOutlined />
          </Fab>
        </Zoom>
      </Container>
    </ErrorBoundary>
  );
};

export default BrowsePage;