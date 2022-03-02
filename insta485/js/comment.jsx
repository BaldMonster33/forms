import React from 'react';
import PropTypes from 'prop-types';

function Comment(props) {
  const {
    lognameOwnsThis,
    owner,
    ownerShowUrl,
    text,
    commentid,
    clickHandler,
    pid,
  } = props;
  return (
    <div>
      <a href={ownerShowUrl}>{owner}</a>
      <span>{text}</span>
      {lognameOwnsThis
        && (
          <button
            type="submit"
            onClick={() => {
              clickHandler(commentid, pid);
            }}
            className="delete-comment-button"
          >
            Delete
          </button>
        )}

    </div>
  );
}

Comment.propTypes = {
  lognameOwnsThis: PropTypes.bool.isRequired,
  owner: PropTypes.string.isRequired,
  ownerShowUrl: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired,
  commentid: PropTypes.number.isRequired,
  clickHandler: PropTypes.func.isRequired,
  pid: PropTypes.number.isRequired,
};

export default Comment;
