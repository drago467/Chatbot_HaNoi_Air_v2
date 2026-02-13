-- Migration: Thêm cột admin_path vào locations
-- Format: "Hà Nội > Quận Cầu Giấy > Phường Dịch Vọng"
-- Dùng để hiển thị hierarchy trong chatbot response

ALTER TABLE locations
ADD COLUMN IF NOT EXISTS admin_path TEXT;

-- Index để tìm kiếm nhanh theo admin_path
CREATE INDEX IF NOT EXISTS idx_locations_admin_path 
ON locations (admin_path) 
WHERE admin_path IS NOT NULL;

-- Comment
COMMENT ON COLUMN locations.admin_path IS 'Đường dẫn hành chính: "Hà Nội > Quận X > Phường Y"';
