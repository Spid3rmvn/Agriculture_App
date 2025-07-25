// components/Posts/PostDetail.jsx
import React from 'react';
import PropTypes from 'prop-types';
import './posts.css';

import mockPostData from '../../utils/mockPostData';

const PostDetail = ({ post = mockPostData }) => {
  if (!post) return <p>Loading post...</p>;

  return (
    <div className="post-detail">
      <img src={post.featured_image_url || '/fallback.jpg'} alt={post.title} className="detail-image" />
      <h1>{post.title}</h1>
      <p className="excerpt">{post.excerpt}</p>

      <div className="author-bar">
        <img src={post.author?.avatar_url || '/default-avatar.png'} alt={post.author?.name} className="avatar" />
        <span>{post.author?.name || 'Anonymous'} • {new Date(post.published_at).toLocaleDateString()}</span>
        {post.category && <span className="category">{post.category.name}</span>}
      </div>
      

      <div className="context-badges">
        {post.related_crops && Array.isArray(post.related_crops) && post.related_crops.map(crop => (
          <span className="badge crop" key={crop}>{crop}</span>
        ))}
        {post.season_relevance && <span className="badge season">{post.season_relevance}</span>}
        {post.applicable_locations && Array.isArray(post.applicable_locations) && post.applicable_locations.map(loc => (
          <span className="badge location" key={loc}>{loc}</span>
        ))}
      </div>


      <div className="post-content" dangerouslySetInnerHTML={{ __html: post.content }} />

      <div className="post-stats">
        <span>👁️ {post.view_count}</span>
        <span>❤️ {post.like_count}</span>
        <span>💬 {post.comment_count}</span>
      </div>
    </div>
  );
};

PostDetail.propTypes = {
    post: PropTypes.shape({
        title: PropTypes.string.isRequired,
        excerpt: PropTypes.string.isRequired,
        featured_image_url: PropTypes.string,
        author: PropTypes.shape({
            name: PropTypes.string,
            avatar_url: PropTypes.string,
        }),
        published_at: PropTypes.string.isRequired,
        category: PropTypes.shape({
            name: PropTypes.string,
        }),
        related_crops: PropTypes.arrayOf(PropTypes.string),
        season_relevance: PropTypes.string,
        applicable_locations: PropTypes.arrayOf(PropTypes.string),
        content: PropTypes.string.isRequired,
        view_count: PropTypes.number,
        like_count: PropTypes.number,
        comment_count: PropTypes.number,
    }),
};

export default PostDetail;