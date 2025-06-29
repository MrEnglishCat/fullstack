"use client";

import {useState, useEffect} from "react";
import styles from "@/components/FilterMinRating/FilterMinRating.module.css"


export default function FilterMinReview({minReviews, setMinReviews, setCurrentPage=()=>{}}) {


    const handleChange = (e) => {
        const value = parseFloat(e.target.value || 0);
        setMinReviews(value);
        setCurrentPage(1)

    };


    return (
        <div className={styles.mainWrapper}>
            <div className="flex flex-col">
                <label htmlFor="minRating" className="mb-2 font-medium">
                    Минимальное количество отзывов:
                </label>
                <input
                    id="minRating"
                    type="number"
                    min="0"
                    step="50"
                    value={minReviews}
                    onChange={handleChange}
                    className="border border-gray-300 rounded px-3 py-2 w-full"
                />
                <p className="mt-2 text-sm text-gray-600">Текущий фильтр: {minReviews}</p>
            </div>
        </div>
    );
}