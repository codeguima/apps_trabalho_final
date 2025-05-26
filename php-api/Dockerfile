FROM php:8.2-cli

# Instala ferramentas necessárias
RUN apt-get update && apt-get install -y unzip curl libzip-dev

# Instala extensões PHP necessárias
RUN docker-php-ext-install sockets zip

# Instala Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /var/www/html

COPY . .

# Instala dependências do Composer
RUN composer install

CMD ["php", "-S", "0.0.0.0:8000", "-t", "."]
