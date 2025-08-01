import React, { useEffect } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { getPost, getComments, clearCurrentPost } from '../../store/slices/postsSlice';
import LoadingSpinner from '../../components/common/LoadingSpinner/LoadingSpinner';
import ErrorMessage from '../../components/common/ErrorMessage/ErrorMessage';
import CommentSection from '../../components/posts/CommentSection';
import Image from '../../components/common/Image/Image';
import FollowButton from '../../components/common/FollowButton/FollowButton';
import { Calendar } from 'lucide-react';
import '../../components/posts/posts.css';

const PostDetailPage = () => {
  const { postId } = useParams();
  const dispatch = useDispatch();
  const location = useLocation();
  const { currentPost, postComments, isLoading, isError, message } = useSelector(state => state.posts);
  const currentUser = useSelector(state => state.auth.user);

  useEffect(() => {
    // Basic validation for postId to prevent API calls with 'create'
    const isValidPostId = postId && postId !== 'create' && postId.length > 5; // A simple check, assuming UUIDs are longer than 'create'

    if (isValidPostId) {
      dispatch(getPost(postId));
      dispatch(getComments(postId));
    }
    
    return () => {
      dispatch(clearCurrentPost());
    };
  }, [dispatch, postId]);

  useEffect(() => {
    if (location.hash === '#comments' && !isLoading) {
      const element = document.getElementById('comments');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }, [location.hash, isLoading]);

  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric', month: 'long', day: 'numeric'
    });
  };

  if (isLoading && !currentPost) {
    return <div className="container"><LoadingSpinner text="Loading post..." /></div>;
  }

  const handleRetry = () => {
    if (postId) {
      dispatch(getPost(postId));
      dispatch(getComments(postId));
    }
  };

  if (isError) {
    return <div className="container"><ErrorMessage message={message || 'Failed to load post.'} onRetry={handleRetry} /></div>;
  }

  if (!currentPost) {
    return <div className="container"><p>Post not found.</p></div>;
  }

  const comments = postComments[postId] || [];

  return (
    <div className="post-detail-page">
      <article className="post-detail">
        {currentPost.featured_image_url && (
          <Image src={currentPost.featured_image_url} alt={currentPost.title || 'Post image'} className="detail-image" fallbackType="post" />
        )}
        <h1>{currentPost.title || 'Untitled Post'}</h1>
        <div className="author-bar">
          <Image src={currentPost.author?.avatar_url} alt={currentPost.author?.name || 'Author'} className="avatar" fallbackType="avatar" />
          <div className="author-info">
            <strong>{currentPost.author?.name || 'Unknown Author'}</strong>
            <small><Calendar size={14} /> Published on {formatDate(currentPost.published_at || currentPost.created_at)}</small>
          </div>
          <div className="author-actions">
            {currentPost.category && <span className="category">{currentPost.category.name}</span>}
            {/* Follow Button for post author */}
            {currentUser && currentUser.user_id !== currentPost.author?.user_id && currentPost.author?.user_id && (
              <FollowButton 
                userId={currentPost.author.user_id}
                initialFollowState={currentPost.author.is_following}
                showStats={false}
                size="medium"
              />
            )}
          </div>
        </div>
        <div className="post-content" dangerouslySetInnerHTML={{ __html: currentPost.content || '<p>No content available</p>' }} />
      </article>
      
      <CommentSection postId={postId} comments={comments} />
    </div>
  );
};

export default PostDetailPage;
