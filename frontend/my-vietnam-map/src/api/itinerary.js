// frontend/src/api/itinerary.js

const API_BASE_URL = 'http://localhost:8000';

/**
 * Gửi yêu cầu tạo lịch trình tới backend
 * @param {Object} itineraryData - Dữ liệu lịch trình
 * @returns {Promise} - Promise chứa kết quả lịch trình
 */
export async function generateItinerary(itineraryData) {
    try {
        // Sửa URL endpoint cho đúng với cấu trúc API của bạn
        const response = await fetch(`${API_BASE_URL}/itinerary/itinerary/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(itineraryData)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`API Error (${response.status}): ${errorText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Lỗi khi tạo lịch trình:', error);
        throw error;
    }
}

/**
 * Format dữ liệu lịch trình từ API thành cấu trúc hiển thị
 * @param {Object} apiResponse - Response từ API
 * @returns {Object} - Dữ liệu lịch trình đã format
 */
export function formatItineraryData(apiResponse) {
    console.log('Raw API response:', apiResponse); // Debug log
    
    if (!apiResponse) {
        console.error('API response is empty');
        return null;
    }

    // Kiểm tra cấu trúc response khác nhau
    let itinerary;
    if (apiResponse.itinerary) {
        // Case 1: Response có trường itinerary (theo code hiện tại)
        itinerary = apiResponse.itinerary;
    } else if (apiResponse.days) {
        // Case 2: Response trực tiếp là itinerary
        itinerary = apiResponse;
    } else {
        console.error('API response không có cấu trúc itinerary hợp lệ:', apiResponse);
        return null;
    }

    const result = {
        summary: {
            province: itinerary.province || apiResponse.province || '',
            totalDays: itinerary.days || itinerary.total_days || 0,
            totalPlaces: 0,
            pace: itinerary.pace || itinerary.travel_pace || 'medium'
        },
        days: [],
        rawData: apiResponse
    };

    // Kiểm tra nếu có itinerary.text (định dạng text)
    if (itinerary.text) {
        // Parse các ngày từ itinerary text
        const daySections = itinerary.text.split(/Ngày \d+:/g).filter(section => section.trim());

        daySections.forEach((section, index) => {
            const dayNumber = index + 1;
            const lines = section.split('\n').filter(line => line.trim());
            
            const places = lines
                .filter(line => line.includes('-') || line.includes('→'))
                .map(line => {
                    // Extract place name từ line
                    let placeName = line
                        .replace(/^- /, '')
                        .replace(/^→ /, '')
                        .replace(/\(.*?\)/g, '')
                        .trim();

                    // Tìm thông tin chi tiết từ filtered_places (nếu có)
                    let placeDetail = null;
                    if (itinerary.filtered_places) {
                        placeDetail = itinerary.filtered_places.find(p => 
                            placeName.includes(p.name) || (p.name && p.name.includes(placeName))
                        );
                    }

                    return {
                        name: placeName,
                        detail: placeDetail || null,
                        time: extractTimeFromLine(line),
                        description: placeDetail?.description || placeDetail?.highlights?.[0] || '',
                        category: placeDetail?.category || '',
                        rating: 0,
                        location: placeDetail?.address || '',
                        coordinates: placeDetail?.latitude && placeDetail?.longitude 
                            ? { lat: placeDetail.latitude, lng: placeDetail.longitude } 
                            : null
                    };
                })
                .filter(place => place.name && place.name.trim());

            if (places.length > 0) {
                result.summary.totalPlaces += places.length;
                result.days.push({
                    dayNumber,
                    date: null, // Sẽ được tính sau
                    places,
                    notes: extractNotesFromSection(section)
                });
            }
        });
    } 
    // Kiểm tra nếu có cấu trúc days trực tiếp
    else if (itinerary.days && Array.isArray(itinerary.days)) {
        // Case: API trả về cấu trúc days trực tiếp
        itinerary.days.forEach((dayData, index) => {
            const dayNumber = index + 1;
            const places = [];
            
            // Xử lý các địa điểm trong ngày
            if (dayData.places && Array.isArray(dayData.places)) {
                dayData.places.forEach(place => {
                    places.push({
                        name: place.name || '',
                        detail: place,
                        time: place.time || place.duration_recommend || '',
                        description: place.description || place.highlights?.[0] || '',
                        category: place.category || '',
                        rating: 0,
                        location: place.address || '',
                        coordinates: place.latitude && place.longitude 
                            ? { lat: place.latitude, lng: place.longitude } 
                            : null
                    });
                });
            }
            
            if (places.length > 0) {
                result.summary.totalPlaces += places.length;
                result.days.push({
                    dayNumber,
                    date: null,
                    places,
                    notes: dayData.notes || extractNotesFromDay(dayData)
                });
            }
        });
    }
    // Kiểm tra nếu có daily_itineraries
    else if (itinerary.daily_itineraries && Array.isArray(itinerary.daily_itineraries)) {
        itinerary.daily_itineraries.forEach((dayItinerary, index) => {
            const dayNumber = index + 1;
            const places = [];
            
            if (dayItinerary.places && Array.isArray(dayItinerary.places)) {
                dayItinerary.places.forEach(place => {
                    places.push({
                        name: place.name || '',
                        detail: place,
                        time: place.time || place.visit_time || '',
                        description: place.description || place.highlights?.[0] || '',
                        category: place.category || '',
                        rating: 0,
                        location: place.address || '',
                        coordinates: place.latitude && place.longitude 
                            ? { lat: place.latitude, lng: place.longitude } 
                            : null
                    });
                });
            }
            
            if (places.length > 0) {
                result.summary.totalPlaces += places.length;
                result.days.push({
                    dayNumber,
                    date: null,
                    places,
                    notes: dayItinerary.notes || []
                });
            }
        });
    }

    // Nếu không có days nào được tạo, tạo cấu trúc mặc định
    if (result.days.length === 0 && itinerary.filtered_places) {
        console.log('Creating default day structure from filtered_places');
        result.days.push({
            dayNumber: 1,
            date: null,
            places: itinerary.filtered_places.map(place => ({
                name: place.name || '',
                detail: place,
                time: place.duration_recommend || '',
                description: place.description || place.highlights?.[0] || '',
                category: place.category || '',
                rating: 0,
                location: place.address || '',
                coordinates: place.latitude && place.longitude 
                    ? { lat: place.latitude, lng: place.longitude } 
                    : null
            })),
            notes: []
        });
        result.summary.totalPlaces = itinerary.filtered_places.length;
    }

    console.log('Formatted itinerary:', result);
    return result;
}

/**
 * Trích xuất thời gian từ dòng text
 */
function extractTimeFromLine(line) {
    const timeMatch = line.match(/(\d{1,2}[:.]\d{2}|\d{1,2}\s*(giờ|h|AM|PM|sáng|chiều|tối))/i);
    return timeMatch ? timeMatch[0] : '';
}

/**
 * Trích xuất ghi chú từ section
 */
function extractNotesFromSection(section) {
    const notes = [];
    const lines = section.split('\n');
    
    lines.forEach(line => {
        if (line.includes('Ghi chú:') || line.includes('Lưu ý:') || line.includes('Note:')) {
            notes.push(line.replace(/Ghi chú:|Lưu ý:|Note:/i, '').trim());
        }
    });
    
    return notes;
}

/**
 * Trích xuất ghi chú từ day object
 */
function extractNotesFromDay(dayData) {
    const notes = [];
    
    if (dayData.notes && Array.isArray(dayData.notes)) {
        return dayData.notes;
    }
    
    if (dayData.tips) {
        if (Array.isArray(dayData.tips)) {
            return dayData.tips;
        } else if (typeof dayData.tips === 'string') {
            return [dayData.tips];
        }
    }
    
    return notes;
}

/**
 * Tính toán ngày dựa trên ngày bắt đầu
 * @param {Date} startDate - Ngày bắt đầu
 * @param {number} totalDays - Tổng số ngày
 * @returns {Array} - Mảng các ngày
 */
export function calculateDates(startDate, totalDays) {
    if (!startDate || !totalDays) return [];
    
    const dates = [];
    const currentDate = new Date(startDate);
    
    for (let i = 0; i < totalDays; i++) {
        const dateCopy = new Date(currentDate);
        dateCopy.setDate(dateCopy.getDate() + i);
        dates.push(dateCopy);
    }
    
    return dates;
}

/**
 * Format date thành string dd/mm/yyyy
 */
export function formatDate(date) {
    if (!date) return '';
    
    // Nếu date là string, chuyển thành Date object
    const d = date instanceof Date ? date : new Date(date);
    
    // Kiểm tra date hợp lệ
    if (isNaN(d.getTime())) return '';
    
    return `${d.getDate().toString().padStart(2, '0')}/${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getFullYear()}`;
}

/**
 * Helper function để tạo dữ liệu test nếu API không hoạt động
 */
export function getMockItineraryData() {
    return {
        itinerary: {
            province: "Quảng Bình",
            days: 3,
            pace: "medium",
            text: `Ngày 1:
- Hang Sơn Đoòng (8:00 - 16:00)
- Động Phong Nha (17:00 - 19:00)
Ghi chú: Mang theo đồ đi mưa

Ngày 2:
- Biển Nhật Lệ (7:00 - 12:00)
→ Suối nước nóng Bang (14:00 - 17:00)
Lưu ý: Cẩn thận khi tắm biển

Ngày 3:
- Vườn quốc gia Phong Nha - Kẻ Bàng (9:00 - 15:00)
- Tham quan làng chài (16:00 - 18:00)`,
            filtered_places: [
                {
                    name: "Hang Sơn Đoòng",
                    category: "Thiên nhiên",
                    address: "Vườn quốc gia Phong Nha - Kẻ Bàng",
                    description: "Hang động tự nhiên lớn nhất thế giới"
                },
                {
                    name: "Động Phong Nha",
                    category: "Thiên nhiên",
                    address: "Phong Nha, Quảng Bình",
                    description: "Động nước đẹp nổi tiếng"
                }
            ]
        }
    };
}