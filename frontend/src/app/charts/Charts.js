"use client";

import PriceHistogram from '@/components/PriceHistogram/PriceHistogram';
import DiscountVsRatingLineChart from '@/components/DiscountVsRatingLineChart/DiscountVsRatingLineChart';
import RangeSlider from "@/components/slider/templateSlider";
import FilterMinRating from "@/components/FilterMinRating/FilterMinRating";
import FilterMinReview from "@/components/FilterMinReview/FilterMinReview";
import { useEffect, useState } from "react";
import {fetchRangeValues} from "@/utils/utils";

export default function Home() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [priceRange, setPriceRange] = useState([0.0, 10.0]);

    const [minRating, setMinRating] = useState(3);
    const [rangeValues, setRangeValue] = useState([0.0, 10.0]);
    const [step, setStep] = useState(10);

    const [minReviews, setMinReviews] = useState(0);


    useEffect(() => {
        fetchRangeValues(setRangeValue, "price")

    }, []);


    useEffect(() => {

        const fetchProducts = async () => {
            try {
                const res = await fetch(
                    `http://localhost:8000/api/products?is_statistic=True&min_price=${priceRange[0]}&max_price=${priceRange[1]}&rating_from=${minRating}&min_review_count=${minReviews}`
                );
                if (!res.ok) throw new Error("Ошибка загрузки данных");
                const data = await res.json();
                setProducts(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();

    }, [priceRange, minRating, minReviews]);

    if (loading) return <div>Загрузка...</div>;
    if (error) return <div>Ошибка: {error}</div>;

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Анализ товаров</h1>

            <div className="flex flex-row gap-5 mb-6">
                <RangeSlider
                    rangeValues={rangeValues}
                    priceRange={priceRange}
                    setPriceRange={setPriceRange}
                    step={step}
                    setStep={setStep}
                />

                <FilterMinRating
                    setProducts={setProducts}
                    minRating={minRating}
                    setMinRating={setMinRating}
                />

                <FilterMinReview
                    setProducts={setProducts}
                    minReviews={minReviews}
                    setMinReviews={setMinReviews}

                />
            </div>

            <div className="flex gap-10">
                <PriceHistogram data={products} />
                <DiscountVsRatingLineChart data={products} />
            </div>
        </div>
    );
}