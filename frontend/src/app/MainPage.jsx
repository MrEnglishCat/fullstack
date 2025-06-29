"use client";

import {useEffect, useState} from "react";
import RangeSlider from "@/components/slider/templateSlider";
import FilterMinRating from "@/components/FilterMinRating/FilterMinRating";
import FilterMinReview from "@/components/FilterMinReview/FilterMinReview";
import {fetchRangeValues} from "@/utils/utils";

export default function Product() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [orderByName, setOrderByName] = useState("name");
    const [orderByPrice, setOrderByPrice] = useState("price");
    const [orderBySalePrice, setOrderBySalePrice] = useState("sale_price");
    const [orderByRating, setOrderByRating] = useState("rating");
    const [orderByReview, setOrderByReview] = useState("review_count");

    const [activeSortField, setActiveSortField] = useState("name");
    const [minRating, setMinRating] = useState(4);
    const [rangeValues, setRangeValue] = useState({});
    const [priceValues, setPriceValues] = useState([0.0, 10.0]);
    const [step, setStep] = useState(10);
    const [minReviews, setMinReviews] = useState(0);


    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await fetch(`http://localhost:8000/api/products?page=${currentPage}&size=${itemsPerPage}`);

                if (!res.ok) throw new Error("Ошибка запроса к API.");

                const data = await res.json();
                setProducts(data.items || []);
                setCurrentPage(1)
                setTotalPages(data.pages || 1);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchRangeValues(setRangeValue, "price");
        fetchData();
    }, []);

    useEffect(() => {
        const fetchFilteredProducts = async () => {
            const res = await fetch(
                `http://localhost:8000/api/products?order_by=${activeSortField}&min_price=${priceValues[0]}&max_price=${priceValues[1]}&rating_from=${minRating}&min_review_count=${minReviews}&page=${currentPage}&size=${itemsPerPage}`
            );
            const data = await res.json();
            console.log(data)
            setProducts(data.items || []);
            setTotalPages(data.pages || 1);
        };

        fetchFilteredProducts();

    }, [activeSortField, currentPage, itemsPerPage, priceValues, minRating, minReviews, currentPage, itemsPerPage]);

    const changeOrderOnClick = async (order_by, setter) => {
        let newOrder = order_by.startsWith('-') ? order_by.slice(1) : `-${order_by}`;
        setter(newOrder);
        setActiveSortField(newOrder);
    };

    const goToNextPage = () => {
        if (currentPage < totalPages) {
            setCurrentPage(currentPage + 1);
        }
    };

    const goToPrevPage = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    const handleItemsPerPageChange = (e) => {
        const newLimit = parseInt(e.target.value, 10);
        setItemsPerPage(newLimit);
        setCurrentPage(1);
    };

    if (loading) return <div>Загрузка...</div>;
    if (error) return <div>Ошибка: {error}</div>;

    return (
        <div className="flex flex-col gap-10">
            <div className="flex flex-row gap-5 space-x-1">
                <RangeSlider
                    rangeValues={rangeValues}
                    priceRange={priceValues}
                    setPriceRange={setPriceValues}
                    step={step}
                    setStep={setStep}
                    setCurrentPage={setCurrentPage}
                />
                <FilterMinRating
                    setProducts={setProducts}
                    minRating={minRating}
                    setMinRating={setMinRating}
                    setCurrentPage={setCurrentPage}
                />
                <FilterMinReview
                    setProducts={setProducts}
                    minReviews={minReviews}
                    setMinReviews={setMinReviews}
                    setCurrentPage={setCurrentPage}
                />

                <div className="flex items-end">
                    <label htmlFor="itemsPerPage" className="block text-sm font-medium text-gray-700 mr-2">
                        На странице:
                    </label>
                    <select
                        id="itemsPerPage"
                        value={itemsPerPage}
                        onChange={handleItemsPerPageChange}
                        className="border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value={10} className="text-black">10</option>
                        <option value={50} className="text-black">50</option>
                        <option value={100} className="text-black">100</option>
                    </select>
                </div>
            </div>

            <table className="table-auto w-full text-center">
                <thead className="bg-blue-600 text-white">
                <tr>
                    <th onClick={() => changeOrderOnClick(orderByName, setOrderByName)}
                        className="hover:cursor-pointer">
                        Название {activeSortField === orderByName &&
                        <span>{orderByName.startsWith("-") ? "🔽" : "🔼"}</span>}
                    </th>
                    <th onClick={() => changeOrderOnClick(orderByPrice, setOrderByPrice)}
                        className="hover:cursor-pointer">
                        Цена {activeSortField === orderByPrice &&
                        <span>{orderByPrice.startsWith("-") ? "🔽" : "🔼"}</span>}
                    </th>
                    <th onClick={() => changeOrderOnClick(orderBySalePrice, setOrderBySalePrice)}
                        className="hover:cursor-pointer">
                        Цена со скидкой {activeSortField === orderBySalePrice &&
                        <span>{orderBySalePrice.startsWith("-") ? "🔽" : "🔼"}</span>}
                    </th>
                    <th onClick={() => changeOrderOnClick(orderByRating, setOrderByRating)}
                        className="hover:cursor-pointer">
                        Рейтинг {activeSortField === orderByRating &&
                        <span>{orderByRating.startsWith("-") ? "🔽" : "🔼"}</span>}
                    </th>
                    <th onClick={() => changeOrderOnClick(orderByReview, setOrderByReview)}
                        className="hover:cursor-pointer">
                        Отзывы {activeSortField === orderByReview &&
                        <span>{orderByReview.startsWith("-") ? "🔽" : "🔼"}</span>}
                    </th>
                </tr>
                </thead>
                <tbody className="divide-y divide-gray-700 bg-gray-900 text-white">
                {Array.isArray(products) && products.length > 0 ? (
                    products.map((product) => (
                        <tr key={product.id}
                            className="hover:bg-blue-300 hover:text-gray-900 transition-colors duration-200 cursor-pointer">
                            <td className="px-6 py-4 whitespace-nowrap text-left">{product.name}</td>
                            <td className="px-6 py-4 whitespace-nowrap">{product.price} BYN</td>
                            <td className="px-6 py-4 whitespace-nowrap text-green-700">{product.sale_price} BYN</td>
                            <td className="px-6 py-4 whitespace-nowrap">⭐ {product.rating}</td>
                            <td className="px-6 py-4 whitespace-nowrap">{product.review_count}</td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan="5" className="py-4 text-center">Нет товаров для отображения</td>
                    </tr>
                )}
                </tbody>
            </table>

            <div className="flex justify-center items-center space-x-4 mt-4">
                <button
                    onClick={goToPrevPage}
                    disabled={currentPage === 1}
                    className={`px-4 py-2 rounded ${currentPage === 1 ? 'bg-gray-500' : 'bg-blue-600 hover:bg-blue-700'} text-white`}
                >
                    Предыдущая
                </button>
                <span>Страница {currentPage} из {totalPages}</span>
                <button
                    onClick={goToNextPage}
                    disabled={currentPage === totalPages}
                    className={`px-4 py-2 rounded ${currentPage === totalPages ? 'bg-gray-500' : 'bg-blue-600 hover:bg-blue-700'} text-white`}
                >
                    Следующая
                </button>
            </div>
        </div>
    );
}