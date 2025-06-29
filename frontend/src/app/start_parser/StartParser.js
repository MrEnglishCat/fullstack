"use client";

import { useState } from "react";
import RangeSlider from "@/components/slider/templateSlider";
import FilterMinRating from "@/components/FilterMinRating/FilterMinRating";
import FilterMinReview from "@/components/FilterMinReview/FilterMinReview";
import PriceHistogram from '@/components/PriceHistogram/PriceHistogram';
import DiscountVsRatingLineChart from '@/components/DiscountVsRatingLineChart/DiscountVsRatingLineChart';

export default function Home() {
    const [url, setUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleRunParser = async () => {
        if (!url.trim()) {
            setError("Пожалуйста, введите URL");
            setSuccess(null);
            return;
        }

        setLoading(true);
        setError(null);
        setSuccess(null);

        try {
            const response = await fetch(`http://localhost:8000/api/run_parser?url=${url}`);

            if (!response.ok) {
                throw new Error("Ошибка при запуске парсера");
            }

            const data = await response.json();
            console.log(data);
            setSuccess("Парсер успешно запущен!");
        } catch (err) {
            setError(err.message || "Не удалось запустить парсер");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col gap-10 p-6">
            <div>
                <label htmlFor="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Введите URL на категорию товара с WB
                </label>
                <textarea
                    id="message"
                    rows="4"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="Введите URL категории Wildberries..."
                ></textarea>
            </div>

            <button
                onClick={handleRunParser}
                type="button"
                disabled={loading}
                className={`text-white ${
                    loading ? 'bg-blue-400' : 'bg-blue-700 hover:bg-blue-800'
                } focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800`}
            >
                {loading ? "Загрузка..." : "Запустить сбор данных"}
            </button>

            {error && (
                <div className="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
                    <span className="font-medium">Ошибка:</span> {error}
                </div>
            )}

            {success && (
                <div className="p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400" role="alert">
                    <span className="font-medium">Успех:</span> {success}
                </div>
            )}
        </div>
    );
}