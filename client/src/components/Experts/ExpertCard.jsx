import React, { useState } from "react";
import { Star, MapPin, MessageSquare, UserPlus } from "lucide-react";
import ConsultationBooking from "./ConsultationBooking";
import Image from '../common/Image/Image';

const ExpertCard = ({ expert, onFollow, onMessage, isFollowing }) => {
  const [showBookingModal, setShowBookingModal] = useState(false);
  const {
    id,
    name,
    title,
    avatar_url,
    specializations = [],
    rating,
    review_count,
    hourly_rate,
    currency,
    service_areas = [],
    availability_status,
    languages_spoken = [],
  } = expert;

  const handleFollow = () => {
    if (onFollow) onFollow(id);
  };

  const handleMessage = () => {
    if (onMessage) onMessage(id);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 flex flex-col items-center text-center">
      <Image
        src={avatar_url}
        alt={name || title || 'Expert profile picture'}
        className="w-24 h-24 rounded-full object-cover mb-4"
        fallbackType="expert"
      />
      <h3 className="text-xl font-bold text-gray-900">{name}</h3>
      <p className="text-green-700 font-medium mb-2">{title}</p>
      <div className="flex items-center text-yellow-500 mb-2">
        <Star className="w-5 h-5" />
        <span className="ml-1 font-bold">{rating}</span>
        <span className="text-gray-500 ml-2">({review_count} reviews)</span>
      </div>
      <div className="flex flex-wrap justify-center gap-2 mb-4">
        {specializations.slice(0, 3).map((spec) => (
          <span
            key={spec}
            className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs"
          >
            {spec}
          </span>
        ))}
      </div>
      <div className="text-lg font-semibold text-gray-800 mb-4">
        ${hourly_rate} / hour
      </div>
      <button 
        onClick={() => setShowBookingModal(true)}
        className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 mb-2"
        disabled={availability_status === 'unavailable'}
      >
        {availability_status === 'unavailable' ? 'Unavailable' : 'Book Consultation'}
      </button>
      <div className="flex w-full gap-2">
        <button
          onClick={handleFollow}
          className={`w-full flex items-center justify-center px-4 py-2 rounded-md text-sm ${
            isFollowing
              ? "bg-gray-200 text-gray-800"
              : "bg-blue-100 text-blue-800 hover:bg-blue-200"
          }`}
        >
          <UserPlus className="w-4 h-4 mr-2" />
          {isFollowing ? "Following" : "Follow"}
        </button>
        <button
          onClick={handleMessage}
          className="w-full flex items-center justify-center px-4 py-2 rounded-md text-sm bg-gray-100 text-gray-700 hover:bg-gray-200"
        >
          <MessageSquare className="w-4 h-4 mr-2" />
          Message
        </button>
      </div>

      {/* Consultation Booking Modal */}
      <ConsultationBooking
        expert={expert}
        isOpen={showBookingModal}
        onClose={() => setShowBookingModal(false)}
      />
    </div>
  );
};

export default ExpertCard;
