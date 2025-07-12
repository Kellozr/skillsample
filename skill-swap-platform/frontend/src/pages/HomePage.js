import React from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Avatar,
  Chip,
  Paper,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  TrendingUpOutlined,
  PeopleOutlined,
  SchoolOutlined,
  StarOutlined,
  ArrowForwardOutlined,
  CodeOutlined,
  DesignServicesOutlined,
  LanguageOutlined,
  MusicNoteOutlined,
  RestaurantOutlined,
  CampaignOutlined,
} from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';

const HomePage = () => {
  const { user } = useAuth();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const features = [
    {
      icon: <SchoolOutlined sx={{ fontSize: 40 }} />,
      title: 'Learn Anything',
      description: 'Discover skills from programming to cooking, taught by passionate experts.',
      color: '#667eea',
    },
    {
      icon: <PeopleOutlined sx={{ fontSize: 40 }} />,
      title: 'Connect & Grow',
      description: 'Build meaningful relationships while expanding your knowledge and abilities.',
      color: '#764ba2',
    },
    {
      icon: <TrendingUpOutlined sx={{ fontSize: 40 }} />,
      title: 'Track Progress',
      description: 'Monitor your learning journey with detailed analytics and achievements.',
      color: '#f093fb',
    },
    {
      icon: <StarOutlined sx={{ fontSize: 40 }} />,
      title: 'Quality Assured',
      description: 'All instructors are verified and rated by our community for quality.',
      color: '#f5576c',
    },
  ];

  const categories = [
    { icon: <CodeOutlined />, name: 'Programming', count: '150+ skills', color: '#667eea' },
    { icon: <DesignServicesOutlined />, name: 'Design', count: '80+ skills', color: '#764ba2' },
    { icon: <LanguageOutlined />, name: 'Languages', count: '60+ skills', color: '#f093fb' },
    { icon: <MusicNoteOutlined />, name: 'Music', count: '45+ skills', color: '#f5576c' },
    { icon: <RestaurantOutlined />, name: 'Cooking', count: '35+ skills', color: '#4facfe' },
    { icon: <CampaignOutlined />, name: 'Marketing', count: '70+ skills', color: '#43e97b' },
  ];

  const stats = [
    { number: '10,000+', label: 'Active Learners' },
    { number: '5,000+', label: 'Skills Available' },
    { number: '50,000+', label: 'Successful Matches' },
    { number: '98%', label: 'Satisfaction Rate' },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: { xs: 8, md: 12 },
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
              >
                <Typography
                  variant="h1"
                  sx={{
                    fontSize: { xs: '2.5rem', md: '3.5rem' },
                    fontWeight: 700,
                    mb: 2,
                    lineHeight: 1.2,
                  }}
                >
                  Learn. Teach. 
                  <Box component="span" sx={{ color: '#f093fb' }}>
                    {' '}Connect.
                  </Box>
                </Typography>
                <Typography
                  variant="h5"
                  sx={{
                    mb: 4,
                    opacity: 0.9,
                    fontWeight: 300,
                    lineHeight: 1.6,
                  }}
                >
                  Join the world's largest skill-sharing community. Learn from experts, 
                  teach what you know, and build lasting connections.
                </Typography>
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                  {!user ? (
                    <>
                      <Button
                        component={Link}
                        to="/register"
                        variant="contained"
                        size="large"
                        sx={{
                          bgcolor: 'white',
                          color: 'primary.main',
                          px: 4,
                          py: 1.5,
                          fontSize: '1.1rem',
                          fontWeight: 600,
                          '&:hover': {
                            bgcolor: 'grey.100',
                            transform: 'translateY(-2px)',
                          },
                        }}
                        endIcon={<ArrowForwardOutlined />}
                      >
                        Get Started Free
                      </Button>
                      <Button
                        component={Link}
                        to="/browse"
                        variant="outlined"
                        size="large"
                        sx={{
                          borderColor: 'white',
                          color: 'white',
                          px: 4,
                          py: 1.5,
                          fontSize: '1.1rem',
                          '&:hover': {
                            borderColor: 'white',
                            bgcolor: 'rgba(255,255,255,0.1)',
                          },
                        }}
                      >
                        Explore Skills
                      </Button>
                    </>
                  ) : (
                    <>
                      <Button
                        component={Link}
                        to="/browse"
                        variant="contained"
                        size="large"
                        sx={{
                          bgcolor: 'white',
                          color: 'primary.main',
                          px: 4,
                          py: 1.5,
                          fontSize: '1.1rem',
                          fontWeight: 600,
                          '&:hover': {
                            bgcolor: 'grey.100',
                            transform: 'translateY(-2px)',
                          },
                        }}
                        endIcon={<ArrowForwardOutlined />}
                      >
                        Browse Skills
                      </Button>
                      <Button
                        component={Link}
                        to="/profile"
                        variant="outlined"
                        size="large"
                        sx={{
                          borderColor: 'white',
                          color: 'white',
                          px: 4,
                          py: 1.5,
                          fontSize: '1.1rem',
                          '&:hover': {
                            borderColor: 'white',
                            bgcolor: 'rgba(255,255,255,0.1)',
                          },
                        }}
                      >
                        My Profile
                      </Button>
                    </>
                  )}
                </Box>
              </motion.div>
            </Grid>
            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
              >
                <Box
                  sx={{
                    position: 'relative',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                  }}
                >
                  <Box
                    sx={{
                      width: { xs: 300, md: 400 },
                      height: { xs: 300, md: 400 },
                      borderRadius: '50%',
                      background: 'rgba(255,255,255,0.1)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      position: 'relative',
                    }}
                  >
                    <Typography
                      variant="h2"
                      sx={{
                        fontSize: { xs: '3rem', md: '4rem' },
                        fontWeight: 700,
                        textAlign: 'center',
                      }}
                    >
                      🚀
                    </Typography>
                  </Box>
                </Box>
              </motion.div>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Stats Section */}
      <Container maxWidth="lg" sx={{ py: 6 }}>
        <Grid container spacing={4}>
          {stats.map((stat, index) => (
            <Grid item xs={6} md={3} key={index}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Box textAlign="center">
                  <Typography
                    variant="h3"
                    sx={{
                      fontWeight: 700,
                      color: 'primary.main',
                      mb: 1,
                    }}
                  >
                    {stat.number}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    {stat.label}
                  </Typography>
                </Box>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Features Section */}
      <Box sx={{ bgcolor: 'background.default', py: 8 }}>
        <Container maxWidth="lg">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Typography
              variant="h2"
              textAlign="center"
              sx={{ mb: 2, fontWeight: 700 }}
            >
              Why Choose SkillSwap?
            </Typography>
            <Typography
              variant="h6"
              textAlign="center"
              color="text.secondary"
              sx={{ mb: 6, maxWidth: 600, mx: 'auto' }}
            >
              Experience the future of learning with our innovative platform designed 
              for modern skill sharing and community building.
            </Typography>
          </motion.div>

          <Grid container spacing={4}>
            {features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  whileHover={{ y: -5 }}
                >
                  <Card
                    sx={{
                      height: '100%',
                      textAlign: 'center',
                      p: 3,
                      transition: 'all 0.3s ease-in-out',
                      '&:hover': {
                        boxShadow: 6,
                      },
                    }}
                  >
                    <Avatar
                      sx={{
                        bgcolor: feature.color,
                        width: 80,
                        height: 80,
                        mx: 'auto',
                        mb: 2,
                      }}
                    >
                      {feature.icon}
                    </Avatar>
                    <Typography variant="h6" gutterBottom fontWeight={600}>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </Card>
                </motion.div>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Categories Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Typography
            variant="h2"
            textAlign="center"
            sx={{ mb: 2, fontWeight: 700 }}
          >
            Popular Categories
          </Typography>
          <Typography
            variant="h6"
            textAlign="center"
            color="text.secondary"
            sx={{ mb: 6 }}
          >
            Explore thousands of skills across diverse categories
          </Typography>
        </motion.div>

        <Grid container spacing={3}>
          {categories.map((category, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ scale: 1.02 }}
              >
                <Paper
                  elevation={2}
                  sx={{
                    p: 3,
                    textAlign: 'center',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease-in-out',
                    background: `linear-gradient(135deg, ${category.color}15 0%, ${category.color}05 100%)`,
                    border: `1px solid ${category.color}20`,
                    '&:hover': {
                      boxShadow: 4,
                      transform: 'translateY(-2px)',
                    },
                  }}
                >
                  <Avatar
                    sx={{
                      bgcolor: category.color,
                      width: 60,
                      height: 60,
                      mx: 'auto',
                      mb: 2,
                    }}
                  >
                    {category.icon}
                  </Avatar>
                  <Typography variant="h6" gutterBottom fontWeight={600}>
                    {category.name}
                  </Typography>
                  <Chip
                    label={category.count}
                    size="small"
                    sx={{
                      bgcolor: category.color,
                      color: 'white',
                      fontWeight: 600,
                    }}
                  />
                </Paper>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* CTA Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: 8,
        }}
      >
        <Container maxWidth="md">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Typography
              variant="h2"
              textAlign="center"
              sx={{ mb: 2, fontWeight: 700 }}
            >
              Ready to Start Your Journey?
            </Typography>
            <Typography
              variant="h6"
              textAlign="center"
              sx={{ mb: 4, opacity: 0.9 }}
            >
              Join thousands of learners and teachers who are already transforming 
              their lives through skill sharing.
            </Typography>
            <Box textAlign="center">
              {!user ? (
                <Button
                  component={Link}
                  to="/register"
                  variant="contained"
                  size="large"
                  sx={{
                    bgcolor: 'white',
                    color: 'primary.main',
                    px: 6,
                    py: 2,
                    fontSize: '1.2rem',
                    fontWeight: 600,
                    '&:hover': {
                      bgcolor: 'grey.100',
                      transform: 'translateY(-2px)',
                    },
                  }}
                  endIcon={<ArrowForwardOutlined />}
                >
                  Join SkillSwap Today
                </Button>
              ) : (
                <Button
                  component={Link}
                  to="/browse"
                  variant="contained"
                  size="large"
                  sx={{
                    bgcolor: 'white',
                    color: 'primary.main',
                    px: 6,
                    py: 2,
                    fontSize: '1.2rem',
                    fontWeight: 600,
                    '&:hover': {
                      bgcolor: 'grey.100',
                      transform: 'translateY(-2px)',
                    },
                  }}
                  endIcon={<ArrowForwardOutlined />}
                >
                  Explore Skills Now
                </Button>
              )}
            </Box>
          </motion.div>
        </Container>
      </Box>
    </Box>
  );
};

export default HomePage;