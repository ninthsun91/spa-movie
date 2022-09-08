componentPosition = (tagId) => {
  const { left: x, top: y } = $("#" + tagId).offset();
  return { x, y };
};
