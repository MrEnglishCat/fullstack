"use client";

import styles from "./TemplateSlider.module.css";
import React, {useEffect, useState} from "react";
import {Range} from "react-range";

export default function RangeSlider({
                                        sliderName = "Фильтр цены",
                                        sliderId = "priceSlider",
                                        rangeValues,
                                        priceRange,
                                        setPriceRange,
                                        step,
                                        setStep,
                                        setCurrentPage = () => {
                                        }
                                    }) {
    const [initialized, setInitialized] = useState(false);

    useEffect(() => {
        if (!rangeValues || typeof rangeValues !== "object") return;

        const {min_value, max_value} = rangeValues;
        if (typeof min_value !== "number" || typeof max_value !== "number") return;

        const safeMin = min_value;
        const safeMax = max_value;

        setPriceRange((prev) => {
            const newMin = prev[0] < safeMin ? safeMin : prev[0];
            const newMax = prev[1] > safeMax ? prev[1] : safeMax;
            return [newMin, newMax];
        });

        const calculatedStep = (safeMax - safeMin) * 0.001;
        setStep(Math.max(0.1, calculatedStep));

        setInitialized(true);
    }, [rangeValues]);

    const handleChange = (newValues) => {
        setPriceRange(newValues);
        setCurrentPage(1)
    };

    if (!initialized) return <div>Загрузка слайдера...</div>;

    return (
        <div className={styles.mainWrapper}>
            <span className="p-3">{sliderName}</span>
            <div className="px-4">
                <Range
                    key={sliderId}
                    values={priceRange}
                    step={step}
                    min={rangeValues.min_value}
                    max={rangeValues.max_value}
                    onChange={handleChange}
                    renderTrack={({props, children}) => (
                        <div {...props} className="h-1 w-full rounded bg-gray-300 relative">
                            <div
                                className="absolute top-1/2 transform -translate-y-1/2 h-8 bg-blue-500 rounded"
                                style={{
                                    left: `${(priceRange[0] / rangeValues.max_value) * 100}%`,
                                    width: `${((priceRange[1] - priceRange[0]) / rangeValues.max_value) * 100}%`,
                                    height: "8px",
                                }}
                            />
                            {children}
                        </div>
                    )}
                    renderThumb={({index, props}) => (
                        <div
                            {...props}
                            className="h-6 w-6 bg-white border-2 border-blue-500 rounded-full focus:outline-none shadow-md"
                            style={{...props.style}}
                            aria-label={`Thumb ${index}`}
                        />
                    )}
                />
                <div className="flex justify-between mt-2 text-sm text-gray-600 gap-12">
                    <span>От: {priceRange[0].toFixed(2)} BYN</span>
                    <span>До: {priceRange[1].toFixed(2)} BYN</span>
                </div>
            </div>
        </div>
    );
}