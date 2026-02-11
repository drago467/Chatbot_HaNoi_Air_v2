"""Data fusion module for Hanoi Air Chatbot.

This module hiện tập trung vào:
- Hợp nhất quan trắc từ nhiều nguồn vào `observations_canonical`
- (Legacy) Hợp nhất forecast; thiết kế mới đã đẩy snapshot forecast trực tiếp
  vào `forecasts_canonical` từ ingestion layer.

Fusion phục vụ chatbot giải thích nguyên nhân ô nhiễm (causal explanations),
không phải đánh giá mô hình dự báo theo thời gian.
"""
