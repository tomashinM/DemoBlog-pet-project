/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export interface Article {
  /** @maxLength 120 */
  title: string;
  /** @pattern ^[-a-zA-Z0-9_]+$ */
  slug: string;
  /** @maxLength 255 */
  description: string;
  body: string;
  tagList: string[];
  author: Profile;
  /** @format date-time */
  createdAt: string;
  /** @format date-time */
  updatedAt: string;
  favorited: boolean;
  favoritesCount: number;
}

export interface ArticleRequest {
  /**
   * @minLength 1
   * @maxLength 120
   */
  title: string;
  /**
   * @minLength 1
   * @maxLength 255
   */
  description: string;
  /** @minLength 1 */
  body: string;
  tagList: string[];
}

export interface BodyError {
  body: string[];
}

export interface Comment {
  id: number;
  body: string;
  author: Profile;
  /** @format date-time */
  createdAt: string;
  /** @format date-time */
  updatedAt: string;
}

export interface CommentRequest {
  /** @minLength 1 */
  body: string;
}

export interface Error {
  errors: BodyError;
}

export interface LoginRequest {
  /**
   * @format email
   * @minLength 1
   */
  email: string;
  /** @minLength 1 */
  password: string;
}

export interface PaginatedArticleList {
  articlesCount: number;
  articles: Article[];
}

export interface PatchedUserRequest {
  bio?: string;
  /**
   * @format uri
   * @maxLength 200
   */
  image?: string | null;
  /**
   * @minLength 1
   * @maxLength 150
   */
  username?: string;
  /**
   * @format email
   * @minLength 1
   * @maxLength 254
   */
  email?: string;
  /**
   * @minLength 1
   * @maxLength 128
   */
  password?: string;
  notifications?: boolean;
}

export interface Profile {
  /** @maxLength 150 */
  username: string;
  /**
   * @format email
   * @maxLength 254
   */
  email: string;
  bio?: string;
  /**
   * @format uri
   * @maxLength 200
   */
  image?: string | null;
  following: boolean;
}

export interface ProfileRequest {
  /**
   * @minLength 1
   * @maxLength 150
   */
  username: string;
  /**
   * @format email
   * @minLength 1
   * @maxLength 254
   */
  email: string;
  bio?: string;
  /**
   * @format uri
   * @maxLength 200
   */
  image?: string | null;
}

export interface Tag {
  tags: string[];
}

export interface User {
  token: string;
  bio?: string;
  /**
   * @format uri
   * @maxLength 200
   */
  image?: string | null;
  /** @maxLength 150 */
  username: string;
  /**
   * @format email
   * @maxLength 254
   */
  email: string;
  notifications?: boolean;
}

export interface UserRequest {
  bio?: string;
  /**
   * @format uri
   * @maxLength 200
   */
  image?: string | null;
  /**
   * @minLength 1
   * @maxLength 150
   */
  username: string;
  /**
   * @format email
   * @minLength 1
   * @maxLength 254
   */
  email: string;
  /**
   * @minLength 1
   * @maxLength 128
   */
  password: string;
  notifications?: boolean;
}

export interface ArticleWrappedArticle {
  article: Article;
}

export interface ArticleWrappedArticleRequest {
  article: ArticleRequest;
}

export interface CommentWrappedComment {
  comment: Comment;
}

export interface CommentWrappedCommentRequest {
  comment: CommentRequest;
}

export interface CommentsWrappedCommentList {
  comments: Comment[];
}

export interface ProfileWrappedProfile {
  profile: Profile;
}

export interface UserWrappedLoginRequest {
  user: LoginRequest;
}

export interface UserWrappedUser {
  user: User;
}

export interface UserWrappedUserPartialRequest {
  user: PatchedUserRequest;
}

export interface UserWrappedUserRequest {
  user: UserRequest;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, "body" | "method" | "query" | "path">;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (securityData: SecurityDataType | null) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "/api/";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) => fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === "number" ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join("&");
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter((key) => "undefined" !== typeof query[key]);
    return keys
      .map((key) => (Array.isArray(query[key]) ? this.addArrayQueryParam(query, key) : this.addQueryParam(query, key)))
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string") ? JSON.stringify(input) : input,
    [ContentType.Text]: (input: any) => (input !== null && typeof input !== "string" ? JSON.stringify(input) : input),
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === "object" && property !== null
              ? JSON.stringify(property)
              : `${property}`,
        );
        return formData;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(`${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`, {
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type && type !== ContentType.FormData ? { "Content-Type": type } : {}),
      },
      signal: (cancelToken ? this.createAbortSignal(cancelToken) : requestParams.signal) || null,
      body: typeof body === "undefined" || body === null ? null : payloadFormatter(body),
    }).then(async (response) => {
      const r = response.clone() as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const data = !responseFormat
        ? r
        : await response[responseFormat]()
            .then((data) => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch((e) => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title BlogAPI
 * @version 1.0.0
 * @baseUrl /api/
 *
 * API of blog
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
  articles = {
    /**
     * @description API endpoints for articles
     *
     * @tags articles
     * @name ArticlesList
     * @request GET:/articles
     * @secure
     */
    articlesList: (
      query?: {
        author?: string;
        favorited?: string;
        /** Number of results to return per page. */
        limit?: number;
        /** The initial index from which to return the results. */
        offset?: number;
        /**
         * Ordering
         *
         * * `created_at` - Created at
         * * `-created_at` - Created at (descending)
         * * `updated_at` - Updated at
         * * `-updated_at` - Updated at (descending)
         * * `favoritesCount` - likes
         * * `-favoritesCount` - likes_desc
         */
        ordering?: (
          | "-created_at"
          | "-favoritesCount"
          | "-updated_at"
          | "created_at"
          | "favoritesCount"
          | "updated_at"
        )[];
        tag?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginatedArticleList, any>({
        path: `/articles`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Create article
     *
     * @tags articles
     * @name ArticlesCreate
     * @request POST:/articles
     * @secure
     */
    articlesCreate: (data: ArticleWrappedArticleRequest, params: RequestParams = {}) =>
      this.request<ArticleWrappedArticle, Error>({
        path: `/articles`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Get an article
     *
     * @tags articles
     * @name ArticlesRetrieve
     * @request GET:/articles/{slug}
     * @secure
     */
    articlesRetrieve: (slug: string, params: RequestParams = {}) =>
      this.request<ArticleWrappedArticle, Error>({
        path: `/articles/${slug}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Update an article
     *
     * @tags articles
     * @name ArticlesUpdate
     * @request PUT:/articles/{slug}
     * @secure
     */
    articlesUpdate: (slug: string, data: ArticleWrappedArticleRequest, params: RequestParams = {}) =>
      this.request<ArticleWrappedArticle, Error>({
        path: `/articles/${slug}`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description API endpoints for articles
     *
     * @tags articles
     * @name ArticlesDestroy
     * @request DELETE:/articles/{slug}
     * @secure
     */
    articlesDestroy: (slug: string, params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/articles/${slug}`,
        method: "DELETE",
        secure: true,
        ...params,
      }),

    /**
     * @description List comments for an article
     *
     * @tags articles
     * @name ArticlesCommentsList
     * @request GET:/articles/{slug}/comments
     * @secure
     */
    articlesCommentsList: (slug: string, params: RequestParams = {}) =>
      this.request<CommentsWrappedCommentList, Error>({
        path: `/articles/${slug}/comments`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Create new comment for an article
     *
     * @tags articles
     * @name ArticlesCommentsCreate
     * @request POST:/articles/{slug}/comments
     * @secure
     */
    articlesCommentsCreate: (slug: string, data: CommentWrappedCommentRequest, params: RequestParams = {}) =>
      this.request<CommentWrappedComment, Error>({
        path: `/articles/${slug}/comments`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description API endpoints for comments
     *
     * @tags articles
     * @name ArticlesCommentsDestroy
     * @request DELETE:/articles/{slug}/comments/{id}
     * @secure
     */
    articlesCommentsDestroy: (id: number, slug: string, params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/articles/${slug}/comments/${id}`,
        method: "DELETE",
        secure: true,
        ...params,
      }),

    /**
     * @description Like/Unlike an article
     *
     * @tags articles
     * @name ArticlesFavoriteCreate
     * @request POST:/articles/{slug}/favorite
     * @secure
     */
    articlesFavoriteCreate: (slug: string, params: RequestParams = {}) =>
      this.request<ArticleWrappedArticle, Error>({
        path: `/articles/${slug}/favorite`,
        method: "POST",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Like/Unlike an article
     *
     * @tags articles
     * @name ArticlesFavoriteDestroy
     * @request DELETE:/articles/{slug}/favorite
     * @secure
     */
    articlesFavoriteDestroy: (slug: string, params: RequestParams = {}) =>
      this.request<ArticleWrappedArticle, Error>({
        path: `/articles/${slug}/favorite`,
        method: "DELETE",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Articles feed
     *
     * @tags articles
     * @name ArticlesFeedList
     * @request GET:/articles/feed
     * @secure
     */
    articlesFeedList: (
      query?: {
        author?: string;
        favorited?: string;
        /** Number of results to return per page. */
        limit?: number;
        /** The initial index from which to return the results. */
        offset?: number;
        /**
         * Ordering
         *
         * * `created_at` - Created at
         * * `-created_at` - Created at (descending)
         * * `updated_at` - Updated at
         * * `-updated_at` - Updated at (descending)
         * * `favoritesCount` - likes
         * * `-favoritesCount` - likes_desc
         */
        ordering?: (
          | "-created_at"
          | "-favoritesCount"
          | "-updated_at"
          | "created_at"
          | "favoritesCount"
          | "updated_at"
        )[];
        tag?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginatedArticleList, Error>({
        path: `/articles/feed`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),
  };
  profiles = {
    /**
     * @description Get profile of a user
     *
     * @tags profiles
     * @name ProfilesRetrieve
     * @request GET:/profiles/{username}
     * @secure
     */
    profilesRetrieve: (username: string, params: RequestParams = {}) =>
      this.request<ProfileWrappedProfile, Error>({
        path: `/profiles/${username}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Follow/Unfollow a user
     *
     * @tags profiles
     * @name ProfilesFollowCreate
     * @request POST:/profiles/{username}/follow
     * @secure
     */
    profilesFollowCreate: (username: string, params: RequestParams = {}) =>
      this.request<ProfileWrappedProfile, Error>({
        path: `/profiles/${username}/follow`,
        method: "POST",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Follow/Unfollow a user
     *
     * @tags profiles
     * @name ProfilesFollowDestroy
     * @request DELETE:/profiles/{username}/follow
     * @secure
     */
    profilesFollowDestroy: (username: string, params: RequestParams = {}) =>
      this.request<ProfileWrappedProfile, Error>({
        path: `/profiles/${username}/follow`,
        method: "DELETE",
        secure: true,
        format: "json",
        ...params,
      }),
  };
  search = {
    /**
     * @description Search for articles
     *
     * @tags search
     * @name SearchList
     * @request GET:/search
     * @secure
     */
    searchList: (
      query?: {
        /** Number of results to return per page. */
        limit?: number;
        /** The initial index from which to return the results. */
        offset?: number;
        search?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginatedArticleList, any>({
        path: `/search`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Base document ViewSet.
     *
     * @tags search
     * @name SearchRetrieve
     * @request GET:/search/{slug}
     * @secure
     */
    searchRetrieve: (slug: string, params: RequestParams = {}) =>
      this.request<Article, any>({
        path: `/search/${slug}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),
  };
  tags = {
    /**
     * @description List of most popular tags
     *
     * @tags tags
     * @name TagsRetrieve
     * @request GET:/tags
     * @secure
     */
    tagsRetrieve: (params: RequestParams = {}) =>
      this.request<Tag, Error>({
        path: `/tags`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),
  };
  user = {
    /**
     * @description Access to current user info
     *
     * @tags user
     * @name UserRetrieve
     * @request GET:/user
     * @secure
     */
    userRetrieve: (params: RequestParams = {}) =>
      this.request<UserWrappedUser, Error>({
        path: `/user`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Update current user info
     *
     * @tags user
     * @name UserUpdate
     * @request PUT:/user
     * @secure
     */
    userUpdate: (data: UserWrappedUserPartialRequest, params: RequestParams = {}) =>
      this.request<UserWrappedUser, Error>({
        path: `/user`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),
  };
  users = {
    /**
     * @description Registration endpoint
     *
     * @tags users
     * @name UsersCreate
     * @request POST:/users
     * @secure
     */
    usersCreate: (data: UserWrappedUserRequest, params: RequestParams = {}) =>
      this.request<UserWrappedUser, Error>({
        path: `/users`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Login endpoint
     *
     * @tags users
     * @name UsersLoginCreate
     * @request POST:/users/login
     * @secure
     */
    usersLoginCreate: (data: UserWrappedLoginRequest, params: RequestParams = {}) =>
      this.request<UserWrappedUser, Error>({
        path: `/users/login`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Verification endpoint
     *
     * @tags users
     * @name UsersVerifyRetrieve
     * @request GET:/users/verify/{token}
     * @secure
     */
    usersVerifyRetrieve: (token: string, params: RequestParams = {}) =>
      this.request<User, any>({
        path: `/users/verify/${token}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),
  };
}
