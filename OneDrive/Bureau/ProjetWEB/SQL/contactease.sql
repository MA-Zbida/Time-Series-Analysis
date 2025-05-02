-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 05, 2025 at 10:19 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `contactease`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `category_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `user_id`, `category_name`) VALUES
(2, 1, 'family'),
(3, 1, 'friends'),
(1, 1, 'work');

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `contact_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `category` varchar(50) DEFAULT 'work',
  `initial` varchar(10) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`contact_id`, `user_id`, `first_name`, `last_name`, `phone_number`, `email`, `category`, `initial`, `created_at`, `updated_at`) VALUES
(1, 1, 'John', 'Doe', '123-456-7890', 'john@example.com', 'work', 'JD', '2025-01-05 21:14:38', '2025-01-05 21:14:38'),
(2, 1, 'Jane', 'Smith', '123-456-7891', 'jane@example.com', 'work', 'JS', '2025-01-05 21:14:38', '2025-01-05 21:14:38'),
(3, 1, 'Mom', '', '123-456-7892', 'mom@example.com', 'family', 'M', '2025-01-05 21:14:38', '2025-01-05 21:14:38'),
(4, 1, 'Dad', '', '123-456-7893', 'dad@example.com', 'family', 'D', '2025-01-05 21:14:38', '2025-01-05 21:14:38'),
(5, 1, 'Mike', 'Johnson', '123-456-7894', 'mike@example.com', 'friends', 'MJ', '2025-01-05 21:14:38', '2025-01-05 21:14:38'),
(6, 1, 'Sarah', 'Wilson', '123-456-7895', 'sarah@example.com', 'friends', 'SW', '2025-01-05 21:14:38', '2025-01-05 21:14:38'),
(7, 1, 'Bob', 'Miller', '123-456-7896', 'bob@example.com', 'work', 'BM', '2025-01-05 21:14:38', '2025-01-05 21:14:38'),
(8, 1, 'Sister', '', '123-456-7897', 'sister@example.com', 'family', 'S', '2025-01-05 21:14:38', '2025-01-05 21:14:38');

-- --------------------------------------------------------

--
-- Table structure for table `contact_categories`
--

CREATE TABLE `contact_categories` (
  `contact_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `contact_categories`
--

INSERT INTO `contact_categories` (`contact_id`, `category_id`) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 2),
(5, 3),
(6, 3),
(7, 1),
(8, 2);

-- --------------------------------------------------------

--
-- Table structure for table `remember_tokens`
--

CREATE TABLE `remember_tokens` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `remember_tokens`
--

INSERT INTO `remember_tokens` (`id`, `user_id`, `token`) VALUES
(1, 1, 'a1592c79b8ec9ad0998d442e892a7b63341a843a56647ecd7b2ebf414a2250cb10b21f2e5905f082ba7eefd373f8a938f59f5700b7b6b7ca988dde0eb711e5b2');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password`, `created_at`, `updated_at`) VALUES
(1, 'Zbida', 'itzzbida@gmail.com', '$2y$12$0xcmiV5yJlH2k0V6q.gtKug6ahOGY52.z/xgkwR9bgFUk0XzjVkZe', '2025-01-05 21:14:28', '2025-01-05 21:14:28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`category_name`),
  ADD UNIQUE KEY `user_id_2` (`user_id`,`category_name`);

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`contact_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `contact_categories`
--
ALTER TABLE `contact_categories`
  ADD PRIMARY KEY (`contact_id`,`category_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `remember_tokens`
--
ALTER TABLE `remember_tokens`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `contact_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `remember_tokens`
--
ALTER TABLE `remember_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `contacts`
--
ALTER TABLE `contacts`
  ADD CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `contact_categories`
--
ALTER TABLE `contact_categories`
  ADD CONSTRAINT `contact_categories_ibfk_1` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`contact_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `contact_categories_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE CASCADE;

--
-- Constraints for table `remember_tokens`
--
ALTER TABLE `remember_tokens`
  ADD CONSTRAINT `remember_tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
